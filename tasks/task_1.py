#Assumptions: Will be used iteratively to perform search on multiple names at a time
# Use drugs names to find in drug list

import regex
import sys
sys.path.append("..")
import pandas as pd
from scripts.helpers import jsonl_loader, csv_loader, preprocess_name, get_all_drugs_names, group_drugs_by_first_letter, get_multiple_names, create_drug_references

class MatchDrugNames:

    def __init__(self, drug_filename):
        drug_df = csv_loader(drug_filename)
        self.drug_dict = self.preprocess_drug_data(drug_df)
        self.drug_reference = create_drug_references(drug_df)


    def get_drugs(self, drug_dataframe):
        drug_dataframe['drugs'] = drug_dataframe.intervention_drugs.apply(lambda x: find_drug_names(x))    
        return True

    def preprocess_trial_data(self, trial_dataframe):
        drug_dataframe = trial_dataframe[trial_dataframe.intervention_type == "Drug"]
        drug_dataframe['intervention_drugs'] = drug_dataframe.intervention_name.apply(lambda x: [preprocess_name(y) for y in get_multiple_names(x)])
        return drug_dataframe

    def preprocess_drug_data(self, drug_df):
        drug_list = get_all_drugs_names(drug_df)
        drug_dict = group_drugs_by_first_letter(drug_list)
        return drug_dict
        
    def find_drug_names(self, drug_name, best_guess=False):
        # Full search
        try:
            if drug_name in self.drug_dict[drug_name[0]]:
                return [self.drug_reference[drug_name]]
        except IndexError:
            pass
        except KeyError:
            pass
        
        ## Partial split
        partial_drug_name = drug_name.split()
        parts = []
        for part in partial_drug_name:
            try:
                if part in self.drug_dict[part[0]]:
                    parts.append(self.drug_reference[part])
            except IndexError:
                pass

            except KeyError:
                pass
        
        if parts:
            return parts

        ## Fuzzy Matching
        if best_guess:
            best_guess_match = self.fuzzy_matching(drug_name)
            try:
                if best_guess_match:
                    return [self.drug_reference[best_guess_match]]
            except KeyError:
                pass

        return None

    def fuzzy_matching(self, drug_name):

        error_rate = len(drug_name)//4 if len(drug_name)//4 < 5 else 5
        regex_search_string = r"(?b)(?:\b" + drug_name + r"\b)" + r"{e<=" + str(error_rate) + "}"
        possible_keys = [x for x in self.drug_dict.keys() if x in drug_name]

        for key in possible_keys:
            regex_drug_list = "|".join(x for x in self.drug_dict[key])
            best_guess = regex.search(regex_search_string, regex_drug_list)

            if best_guess:
                return best_guess.group(0)



        # Best match

        # Partial search

        

        



    


