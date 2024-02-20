import multiprocessing
import itertools
import os
import glob
import shutil


import pandas as pnd
import cobra


from gempipe.curate.gaps import perform_gapfilling
from gempipe.curate.gaps import import_from_universe


from ..commons import chunkize_items
from ..commons import load_the_worker
from ..commons import gather_results



def strenghten_uptakes(model): 

    
    for r in model.reactions: 
        if r.lower_bound < 0: 
            r.lower_bound = -1000



def task_strainfiller(file, args):
    
    
    # get the arguments
    panmodel = args['panmodel']
    minflux = args['minflux']
    outdir = args['outdir']
    
    
    # load the strain-specific model
    ss_model = cobra.io.load_json_model(file)

    
    # get the accession
    basename = os.path.basename(file)
    accession, _ = os.path.splitext(basename)
    
    
    # define key objects: 
    inserted_rids = []  # rids needed for gapfilling
    
    
    # go on with gapfilling: 
    first_sol_rids = perform_gapfilling(ss_model, panmodel, minflux=minflux, nsol=1, verbose=False)
    if first_sol_rids == None:  # an exception was raised
        strenghten_uptakes(ss_model)
        strenghten_uptakes(panmodel)
        first_sol_rids = perform_gapfilling(ss_model, panmodel, minflux=minflux, nsol=1, verbose=False)
        
    
    # if still no solution despite the strenghten_uptakes trick:
    if first_sol_rids == None:
        return [{'accession': accession, 'R': '-', 'inserted_rids': '-', 'solver_error': e, 'obj_value_gf': '-', 'status_gf': '-'}]

    
    # if empty solution (no reactions ot add):
    if first_sol_rids == []: 
        # save the model as it is:
        cobra.io.save_json_model(ss_model, f'{outdir}/{accession}.json')
        return [{'accession': accession, 'R': 'same', 'inserted_rids': '-', 'solver_error': '-', 'obj_value_gf': '-', 'status_gf': '-'}]
        
        
    # add the needed reactions:
    for rid in first_sol_rids:
        import_from_universe(ss_model, panmodel, rid, bounds=None, gpr='')
        inserted_rids.append(rid)
    
    
    # get some metrics: 
    n_R = len(ss_model.reactions)
    
    
    # try the FBA: 
    res = ss_model.optimize()
    obj_value = res.objective_value
    status = res.status
    
    
    # save strain specific model to disk
    cobra.io.save_json_model(ss_model, f'{outdir}/{accession}.json')
    
    
    # compose the new row:
    return [{'accession': accession, 'R': n_R, 'inserted_rids': inserted_rids, 'solver_error': '-', 'obj_value_gf': obj_value, 'status_gf': status}]



def get_gapfilling_matrix(results_df, outdir):
    
    
    gf_matrix = []  # list of dictionaries future dataframe
    for accession in results_df.index: 
        inserted_rids = results_df.loc[accession, 'inserted_rids']
        
        
        # populate the tabular results:
        if type(inserted_rids) == str:
            if inserted_rids == '-':  # model not gapfilled.
                gf_matrix.append({'accession': accession})
        else: 
            row_dict = {}
            for rid in inserted_rids:
                row_dict[rid] = 1
            row_dict['accession'] = accession
            gf_matrix.append(row_dict)
            
    
    # convert to dataframe: 
    gf_matrix = pnd.DataFrame.from_records(gf_matrix)
    gf_matrix = gf_matrix.set_index('accession', drop=True)
    gf_matrix = gf_matrix.fillna(0)  # Replace missing values with 0.
    gf_matrix = gf_matrix.astype(int)  # Force from float to int.
    
    
    # save to file:
    gf_matrix.to_csv(outdir + 'gf_matrix.csv')
            


def strain_filler(logger, outdir, cores, panmodel, minflux):
    
    
    # log some messages:
    logger.info("Gap-filling strain-specific models...")

   
    # create output dir
    if os.path.exists(outdir + 'strain_models_gf/'):
        # always overwriting if already existing
        shutil.rmtree(outdir + 'strain_models_gf/')  
    os.makedirs(outdir + 'strain_models_gf/', exist_ok=True)
    

    # create items for parallelization: 
    items = []
    for file in glob.glob(outdir + 'strain_models/*.json'):
        items.append(file)
        
        
    # randomize and divide in chunks: 
    chunks = chunkize_items(items, cores)
    
    
    # initialize the globalpool:
    globalpool = multiprocessing.Pool(processes=cores, maxtasksperchild=1)
    
    
    # start the multiprocessing: 
    results = globalpool.imap(
        load_the_worker, 
        zip(chunks, 
            range(cores), 
            itertools.repeat(['accession', 'R', 'solver_error']), 
            itertools.repeat('accession'), 
            itertools.repeat(logger), 
            itertools.repeat(task_strainfiller),  # will return a new sequences dataframe (to be concat).
            itertools.repeat({'panmodel': panmodel, 'minflux': minflux, 'outdir': outdir + 'strain_models_gf'}),
        ), chunksize = 1)
    all_df_combined = gather_results(results)
    
    
    # empty the globalpool
    globalpool.close() # prevent the addition of new tasks.
    globalpool.join() 
    
    
    # join with the previous table, and save:
    results_df = pnd.read_csv(outdir + 'derive_strains.csv', index_col=0)
    results_df = pnd.concat([results_df, all_df_combined], axis=1)
    results_df.to_csv(outdir + 'derive_strains.csv')
    
    
    # create the gapfilling matrix starting from 'results_df'
    get_gapfilling_matrix(results_df, outdir)
    
    
    return 0