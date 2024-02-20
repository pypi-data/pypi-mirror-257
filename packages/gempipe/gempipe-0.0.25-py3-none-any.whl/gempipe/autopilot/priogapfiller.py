import os
import json
import glob
from importlib import resources


import pandas as pnd
import cobra


from ..commons import read_refmodel


from gempipe.recon.networkrec import filter_alignment
from gempipe.recon.networkrec import get_gene_scores_table
from gempipe.recon.networkrec import get_protein_scores_table
from gempipe.recon.networkrec import get_reaction_scores_table
from gempipe.recon.networkrec import normalize_reaction_scores


from gempipe.recon.refexpansion import add_new_reaction


from gempipe.curate.medium import reset_growth_env
from gempipe.curate.gaps import perform_gapfilling
from gempipe.curate.gaps import import_from_universe



def get_Rset_dataframe(panmodel, reaction_scores, refmodel, universe):
    # The Rset_dataframe is a table listing all the reaction that are currently NOT part of the draft panmodel.
    # These missing reactions may come (1) from the reference model, or (2) from the universe model.
    # The Rset_dataframe will also report lb, ub, n_score (normalized score), and penalty for each of these reactions. 
    
    
    # save the reaction table to the gapfilling folder
    reaction_scores['reaction'] = reaction_scores['reaction'].str[2:]  # remove the 'R_' prefix (eg R_11M3ODO -> 11M3ODO)
    reaction_scores = reaction_scores.set_index('reaction', drop=True, verify_integrity=True)  
    
    
    Rset = set()  # expanding set of processed reactions
    Rset_dataframe = []   # list of dicts, future df. 
    modeled_rids = [r.id for r in panmodel.reactions]
    tabled_rids = list(reaction_scores.index) 
    
    
    # parse the reference and universe model:
    # note: reference reactions have priority over universe reaction as reference comes as first!
    for i, source in enumerate([refmodel, universe]):
        for r in source.reactions:
            if r.id not in modeled_rids:
                if r.id in Rset: 
                    continue  # already coming from the reference
                    
                    
                # some flags: in reference / in reaction scores table:
                in_ref = True if i==0 else False
                in_tab = r.id in tabled_rids
                
                
                # define the nature of this reaction
                is_enzymatic = True
                if len(r.metabolites)==1:  # exclude EX_change , sink, demand reactions. 
                    is_enzymatic = False  
                
                
                # define the (normalized) reaction score for this missing reaction
                n_score = 0  # like 'spontaneous' reactions
                if in_tab: n_score = reaction_scores.loc[r.id, 'normalized_score']
                
                
                # define the penalty for this reaction
                penalty = 1 / (1 + n_score)
                
                
                # populate the dataframe: 
                Rset_dataframe.append({
                    'rid': r.id, 'in_ref': in_ref, 'in_tab': in_tab, 'is_enzymatic': is_enzymatic,
                    'lb': r.lower_bound, 'ub': r.upper_bound, 'n_score': n_score, 'penalty': penalty})
                Rset.add(r.id)
        
            
    # build and save the Rset_dataframe:
    Rset_dataframe = pnd.DataFrame.from_records(Rset_dataframe)
    Rset_dataframe = Rset_dataframe.set_index('rid', drop=True, verify_integrity=True)
    Rset_dataframe = Rset_dataframe.sort_values(by='penalty', ascending=True)  # top scoring on top.
    Rset_dataframe.to_csv('working/gapfilling/Rset_dataframe.csv')
    
    
    return Rset_dataframe



def create_extended_universe(logger, panmodel, Rset_dataframe, refmodel, universe, mancor_filepath):
    # create an 'all_model', starting from the draft pan model, 
    # adding all the missing reactions both from the reference and the universe.
    expanded_universe = panmodel.copy()
    
    # remove all residual genes:
    cobra.manipulation.delete.remove_genes(expanded_universe, [g for g in expanded_universe.genes], remove_reactions=False)
    
    
    # below we use the expand_reference function from refexpansion.py.
    # Therefore we need the same 'addedms_logger', and 'mancor'.
    addedms_logger = open('working/gapfilling/candidate_metabolites.txt', 'w')
    if mancor_filepath != '-': # existence of the file was verified in gempipe.recon
        mancor = mancor_to_dict(logger, mancor_filepath)  # mancor formatting was already veryfied in gempipe.recon
    else: mancor = {'formulas': {}, 'charges': {}, 'reactions': {}, 'blacklist': []}  # emtpy, easier to handle


    # iterate the 'Rset_dataframe' and pick up reactions from the appropriate source:
    reactions_to_add = len(Rset_dataframe)
    cnt_added = 0
    current_percentage = 0
    for rid, row in Rset_dataframe.iterrows(): 
        if row['in_ref'] == True:   
            # then pick up from the reference
            r = refmodel.reactions.get_by_id(rid)
        else: # then pick up from the universe
            r = universe.reactions.get_by_id(rid)
        
        
        # assure that exchange reactions have bounds (0, 1000)
        if len(r.metabolites)==1 and list(r.metabolites)[0].id.endswith('_e'):
            bounds = (0, 1000)
        else: bounds = r.bounds
        
        
        # add the reaction:
        add_new_reaction(r, expanded_universe, addedms_logger, mancor, empty_gpr=True, bounds=bounds)
        cnt_added += 1
            
        
        # log progress
        progress = int(cnt_added/reactions_to_add * 100)
        if progress%10==0 and progress > current_percentage:
            current_percentage = progress
            universe_content = f"G:{len(expanded_universe.genes)}, R:{len(expanded_universe.reactions)}, M:{len(expanded_universe.metabolites)}"
            logger.debug(f"{current_percentage}% ({universe_content})")
        

    # save 'expanded_universe' to feed the later gapfilling.    
    cobra.io.save_json_model(expanded_universe, 'working/gapfilling/expanded_universe.json')
    addedms_logger.close()   # close filestream.
    
    
    return expanded_universe


    
def build_universe_candidates(logger, panmodel, refmodel, refproteome, staining, mancor_filepath):
    # here we basically performe another reaction score computation, like in the 
    # reference-free reconstruction, but this time we do not filter the alignment
    # (or we use really relaxed thresholds):
    logger.debug('Computing new reaction scores used relaxed alignment...')
    alignment_filtered = filter_alignment(logger, identity=10, coverage=40)
    
    
    # load gprm table (gene-to-protein_complex-to-reaction-to-model)
    gprm_table = pnd.read_csv('working/free/gprm_table.csv')
    
    
    # get the 'gene_scores' table:
    gene_scores = get_gene_scores_table(logger, alignment_filtered, gprm_table)
    gene_scores.to_csv('working/gapfilling/gene_scores.csv')
                 
    # get the 'protein_scores' table: 
    protein_scores = get_protein_scores_table(logger, gene_scores)
    protein_scores.to_csv('working/gapfilling/protein_scores.csv')
                 
    # get the 'reaction_scores' table: 
    reaction_scores = get_reaction_scores_table(logger, protein_scores)
    reaction_scores.to_csv('working/gapfilling/reaction_scores.csv')
                 
    # normalize reaction scores:
    reaction_scores_normalized = normalize_reaction_scores(reaction_scores)
    reaction_scores_normalized.to_csv('working/gapfilling/reaction_scores_normalized.csv')
    
    
    # load reference model (if any):
    if refmodel != '-' and refproteome != '-':  # file existance already checked.
        refmodel = read_refmodel(refmodel)
        if type(refmodel)==int: return 1  # an error was raised
    else: refmodel = cobra.Model('empty')
    
    
    # load the universe  (basically it's a wrapper of the recon function):
    from gempipe.recon.networkrec import get_universe_template
    universe = get_universe_template(logger=None, staining=staining)
    
        
    # get the set of universal + reference reactions that are not yet in the draft panmodel
    logger.debug('Gathering candidate gap-filling reactions...')
    Rset_dataframe = get_Rset_dataframe(panmodel, reaction_scores_normalized, refmodel, universe)
        
        
    # add the missing reactions to the panmodel, in order to produce a single, expanded universe.
    logger.debug('Building the expanded universe...')
    expanded_universe = create_extended_universe(logger, panmodel, Rset_dataframe, refmodel, universe, mancor_filepath)
    
    
    return Rset_dataframe, expanded_universe
    
    

def get_media_definitions(logger, media_filepath):
    
    
    logger.debug("Loading the provided media definitions...")
    
    
    media_files = []  # filepaths to json media definitions
    # check if the user specified something:
    if media_filepath != '-':  
        # get the media files:
        if os.path.exists(media_filepath):
            # check if the user specified a folder:
            if os.path.isdir(media_filepath):
                if media_filepath[-1] != '/': media_filepath = media_filepath + '/'
                media_files = glob.glob(media_filepath + '*')
            else:  # the user specified a single file:
                media_files = [media_filepath]
        else:  # path does not exixts (no folder / no file)
            logger.error(f"The path provided for media definitions (-m/--media) does not exists: {media_filepath}.")
            return 1
    else:  # use a predefined built-in minimal medium
        logger.debug("No definitions provided: loading the built-in minimal aerobic medium...")
        with resources.path("gempipe.assets", "minimal_medium.json") as asset_path:  # taken from CarveMe v1.5.2
            media_files = [asset_path]
         
        
    # check the formatting of the media files, producing a single dict contianing all provided media:
    media = {}   # single dict for all media provided
    for file_path in media_files:
        try:
            with open(file_path, 'r') as file:
                medium_data = json.load(file)
                media[medium_data['name']] = {}
                for rid in medium_data['exchanges'].keys():
                    media[medium_data['name']][rid] = medium_data['exchanges'][rid]
        except json.JSONDecodeError as e:
            logger.error(f"The provided medium file (JSON format) {file_path} encountered the following decoding error: {e}.")
            return 1
        
        
    logger.debug(f"Loaded {len(media.keys())} media definitions: {', '.join(list(media.keys()))}.")
    return media
            
    
          
def apply_json_medium(model, medium):
    
    
    reset_growth_env(model)
    for rid in medium.keys():
        try: model.reactions.get_by_id(rid).lower_bound = medium[rid]
        except:  # rid not found inside the 'expanded_universe'
            logger.error(f"The exchange reaction '{rid}' contained in the medium definition '{medium_name}' does not exist in the expanded_universe.")
            return 1
        
    return 0



def strenghten_uptakes(model): 

    
    for r in model.reactions: 
        if r.lower_bound < 0: 
            r.lower_bound = -1000
    
        
    
def check_expuni_growth(logger, expanded_universe, media): 
    
    
    # log some message:
    logger.debug("Testing the growth of the 'expanded_universe' on the provided media...")
    
    
    # iterate the provided media
    for medium_name, medium in media.items():


        # apply the medium recipe:
        response = apply_json_medium(expanded_universe, medium)
        if response == 1: return 1


        # verify the growth of the expanded_universe:
        res = expanded_universe.optimize()
        obj_value = res.objective_value
        status = res.status
        can_growth = res.status=='optimal' and obj_value > 0
        logger.debug(f"'expanded_universe' growth on {medium_name}: {can_growth} ({status}, {obj_value}).")


        # raise error if it cannot grow:
        if not can_growth:
            cobra.io.save_json_model(expanded_universe, 'working/gapfilling/expuni_nogrowth.json')
            logger.error(  # log the error message: 
                f"The medium definition '{medium_name}' is unable to support growth of the 'expanded_universe'. " +
                f"A copy of the 'expanded_universe', trying to grow on the '{medium_name}', is saved in 'working/gapfilling/expuni_nogrowth.json' for you to fix the '{medium_name}' definition.")
            return 1
        
        
    return 0
    
    
    
def prio_gapfilling(logger, panmodel, expanded_universe, media, Rset_dataframe):
    
    
    # log some message:
    logger.debug("Performing prioritized gap-filling (using penalties)...")
    rids_to_add = []
    
    
    # create the penalties dictionary
    logger.debug("Creating the penalty dictionary...")
    penalties = {}
    for r in expanded_universe.reactions: 
        try: penalty = Rset_dataframe.loc[r.id, 'penalty']
        # this reaction was not part of the candidate gapfilling set:
        except: penalty = 0  # no penalty for reactions that are already in the draft pan-model.
        penalties[r.id] = penalty
            

    # iterate the provided media
    for medium_name, medium in media.items():
        
        
        # assure the presence of the needed exchange reactions:
        for exr in medium.keys():
            try: _ = panmodel.reactions.get_by_id(exr)
            except:  # insert this missing exchange
                panmodel.add_reactions([ expanded_universe.reactions.get_by_id(exr)])
                logger.debug(f"The missing exchange reaction '{exr}' was inserted!")
        
        
        # apply medium definition to both the models:
        # 'response' cannot be 1, has it was already checked previously in 'check_expuni_growth' for the 'expanded_universe'.
        _ = apply_json_medium(panmodel, medium)
        _ = apply_json_medium(expanded_universe, medium)
        
        
        # define the minimal flux through the objective, defined as 10% of the 'expanded_universe'
        minflux = 0.1 * expanded_universe.slim_optimize()   
        
        
        # get candidate gapfilling reactions: 
        logger.debug(f"Now gapfilling for medium {medium_name}...")
        first_sol_rids = perform_gapfilling(panmodel, expanded_universe, minflux=minflux, nsol=1, penalties=penalties, verbose=False)
        if first_sol_rids == None:  # an exception was raised
            # try to solve the 'lower integer thresholds' errors etc.
            logger.debug(f"Medium {medium_name}: temporarily strenghtening uptakes for getting thicker signal...")
            strenghten_uptakes(panmodel)
            strenghten_uptakes(expanded_universe)
            minflux = 0.1 * expanded_universe.slim_optimize() 
            first_sol_rids = perform_gapfilling(panmodel, expanded_universe, minflux=minflux, nsol=1, penalties=penalties, verbose=False)
        
        
        # append candidate reactions to the 'rids_to_add' list:
        if first_sol_rids==[]:
            logger.debug(f"Medium {medium_name}: growth was already enabled, no gap-filling reactions needed.")
        else: 
            logger.debug(f"Medium {medium_name}: found these gap-filling reactions: {first_sol_rids}.")
            rids_to_add = rids_to_add + first_sol_rids
            
            
    # insert all the new reactions:
    rids_to_add = list(set(rids_to_add))
    for rid in rids_to_add:
        import_from_universe(panmodel, expanded_universe, rid, gpr='gapfilled')
    
     
    return 0
            
    
    
    

def prio_gapfiller(logger, refmodel, refproteome, staining, mancor_filepath, media_filepath):
    
    
    # create subdirs without overwriting
    os.makedirs('working/gapfilling/', exist_ok=True)
    
    
    # some log messages
    logger.info('Now starting the prioritized gap-filling...')
    
    
    # load draft panmodel: 
    panmodel = cobra.io.load_json_model('working/duplicates/draft_panmodel.json')
    logger.debug(f"Starting with content: G {len(panmodel.genes)} R {len(panmodel.reactions)} M {len(panmodel.metabolites)}")
    
    
    # build the condidate gap-filler list (Rset) and the expanded universe
    Rset_dataframe, expanded_universe = build_universe_candidates(logger, panmodel, refmodel, refproteome, staining, mancor_filepath)
    
    
    # get the list of media on which to gap-fill: 
    media = get_media_definitions(logger, media_filepath)
    if type(media)==int: return 1   # we encountered an error.
    
    
    # check if the 'expanded_universe' can grow in the given list of media.
    response = check_expuni_growth(logger, expanded_universe, media)
    if response == 1: return 1
            
    
    # perform the prioritized gap-filling.
    response = prio_gapfilling(logger, panmodel, expanded_universe, media, Rset_dataframe)
    if response == 1: return 1
    
    
    # OVERWRITE draft pan-model
    cobra.io.save_json_model(panmodel, f'working/duplicates/draft_panmodel.json')
    logger.debug(f"Ending with content: G {len(panmodel.genes)} R {len(panmodel.reactions)} M {len(panmodel.metabolites)}")
    
    
    return 0
    