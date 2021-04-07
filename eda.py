from scripts.helpers import jsonl_loader, csv_loader, get_all_drugs_names, group_drugs_by_first_letter, preprocess_name
import config as cfg

if __name__ == '__main__':

    dataframe = csv_loader(cfg.files["DRUG_NAMES_FILE"])
    print(dataframe.head())

    ## How many words does the longest drug name contain?
    dataframe['word_length'] = dataframe.itemLabel.apply(lambda x: len(x.split()))
    print(f'Longest length: {dataframe.word_length.max()}')

    print('Longest drug name:', dataframe[dataframe.word_length == dataframe.word_length.max()].itemLabel)

    drug_list = get_all_drugs_names(dataframe)
    print(drug_list[:5])
    drug_dict = group_drugs_by_first_letter(drug_list)
    print(drug_dict.keys())
    print(drug_dict['-'])

    ##Assumption: Accented words can be converted for easier processing
    ##Assumption: Only occurences of intervention type: drugs, should be explored.
    
    