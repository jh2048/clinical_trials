import pandas as pd
import unicodedata
import regex as re
import json

def jsonl_loader(filename):
    """
    trial_file: File with JSONL input
    """
    file_io = open(filename)
    json_content = [json.loads(jline) for jline in file_io.read().splitlines()]
    dataframe = pd.DataFrame(json_content)
    return dataframe

def csv_loader(filename):
    dataframe = pd.read_csv(filename, sep = ",", quotechar="\"")
    return dataframe

def get_all_drugs_names(dataframe):
    dataframe['alts'] = dataframe.altLabel_list.apply(lambda x: x.split('|'))
    drug_list = []

    drug_list = [drug for alt_drugs in dataframe['alts'] for drug in alt_drugs]
    drug_list.extend(dataframe.itemLabel)
    drug_list = list(filter(None, drug_list))
    return drug_list

def group_drugs_by_first_letter(drug_list):
    drug_dict = {}
    for drug in drug_list:
        try:
            if len(drug) > 1:
                drug_name = preprocess_name(drug)
                if drug_name[0] in drug_dict:
                    drug_dict[drug_name[0]].append(drug_name)
                else:
                    drug_dict[drug_name[0]] = [drug_name]
        except IndexError:
            pass
    return drug_dict

def preprocess_name(drug_name):
    parentheses_trans = str.maketrans({"(":None, ")":None, "{":None, "}":None, "[":None, "]":None, "/":" ", "\\":" "})
    drug_name = remove_accented_chars(drug_name)
    drug_name = drug_name.translate(parentheses_trans)
    drug_name = drug_name.lower().rstrip().lstrip()
    return drug_name

def get_multiple_names(drug_name):
    drug_names = []
    drug_name = drug_name.split('+')
    for drug in drug_name:
        drug = drug.split('and')
        if len(drug) > 1:
            drug_names.extend(drug)
    return drug_names

def remove_accented_chars(drug_name):
    drug_name = unicodedata.normalize('NFKD', drug_name).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    return drug_name

def create_drug_references(dataframe):
    drug_ref = {}
    dataframe['alts'] = dataframe.altLabel_list.apply(lambda x: x.split('|'))
    drug_ref_df = dataframe[["itemLabel", "alts"]]
    for idx, row in drug_ref_df.iterrows():
        for val in row.alts:
            val = preprocess_name(val)
            label = preprocess_name(row.itemLabel)
            drug_ref[val] = label
        drug_ref[label] = label
    return drug_ref
        