from tasks.task_1 import MatchDrugNames
from scripts.helpers import jsonl_loader
import config as cfg
import argparse

if __name__ == '__main__':
    ## Get input values
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", dest='best_guess', action='store_true')
    parser.add_argument("-n", dest='non_empty', action='store_true')

    args = parser.parse_args()
    ## Include fuzzy matching
    best_guess = True if args.best_guess else False
    ## Only output values which have drug matches
    non_empty = True if args.non_empty else False

    ## import main processes for task 1 and generate drug list and ref
    match = MatchDrugNames(cfg.files["DRUG_NAMES_FILE"])

    ## Load clinical data and preprocess test
    clinical_trial_df = jsonl_loader(cfg.files["CLINICAL_TRIAL_FILE"])
    trial_dataframe = match.preprocess_trial_data(clinical_trial_df)

    output = []

    for idx, row in trial_dataframe.iterrows():
        output_drugs = []
        drugs = row.intervention_drugs
        for drug in drugs:
            match_drug = match.find_drug_names(drug, best_guess=best_guess)
            if match_drug:
                output_drugs.extend(match_drug)
        if not non_empty:
            output.append({"nct_id": row.nct_id, "drugs":output_drugs})
        if non_empty and output_drugs:
            output.append({"nct_id": row.nct_id, "drugs":output_drugs})

    ##Output drug matches
    with open('drug_matches.txt', 'w') as f:
        f.write(str(output))