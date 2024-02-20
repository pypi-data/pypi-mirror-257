import pickle
import os


import pandas as pnd



def create_report(logger, outdir):
    
    
    report = []  # list of dicts, future dataframe
    
    
    # get the retained genomes/proteomes (post filtering):
    with open('working/proteomes/species_to_proteome.pickle', 'rb') as handler:
        species_to_proteome = pickle.load(handler)
        for species in species_to_proteome.keys(): 
            for proteome in species_to_proteome[species]:
                basename = os.path.basename(proteome)
                accession, _ = os.path.splitext(basename)
                
                
                # populate the table: 
                report.append({'species': species, 'accession': accession})
                
                
    # save to file
    report = pnd.DataFrame.from_records(report)
    report.to_csv(outdir + 'report.csv')
    
    
    
    return 0 
    
    