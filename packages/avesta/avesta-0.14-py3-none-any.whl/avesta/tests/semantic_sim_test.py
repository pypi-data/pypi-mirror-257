from pathlib import Path
import pandas as pd
from tqdm import tqdm
from avesta.tools.similarity.semantic_sim import semantic_synonym_checker
from avesta.tools.similarity.lexical_sim import lexical_synonym_checker

# sem_results = []
# lex_results = []
#
# data = pd.read_csv("../../../llm/fine_tune/same_as_dataset.csv")
# data = data[data["result"] == "same"]
# print(len(data))
# for _, row in tqdm(data.iterrows()):
#     sem_res = semantic_synonym_checker(row['one'], row['two'])
#     lex_res = lexical_synonym_checker(row['one'], row['two'])
#     if sem_res == 'Yes':
#         sem_results.append('same')
#     else:
#         sem_results.append('different')
#     if lex_res == 'Yes':
#         lex_results.append('same')
#     else:
#         lex_results.append('different')
#
# print("Total lexical", len([i for i in lex_results if i == "same"]))
# print("Total semantic", len([i for i in sem_results if i == "same"]))
# data['semantic_prediction'] = sem_results
# data['lexical_prediction'] = lex_results
# data.to_csv("../../../llm/fine_tune/same_as_dataset_predicted.csv", index=False)
# semantic_data = data[data["semantic_prediction"]=='same']
# semantic_data = semantic_data.loc[:, ['one','two']]
# print(semantic_data[:10])
syn_data_path = Path(__file__).parent.parent / "resources" / "synonym"

ecom_synonyms = pd.read_csv(Path.joinpath(syn_data_path, "ecom_synonyms.csv"))
for i, j in zip(ecom_synonyms["one"].values.tolist(), ecom_synonyms["two"].values.tolist()):
    for k, l in zip(ecom_synonyms["two"].values.tolist(), ecom_synonyms["one"].values.tolist()):
        if (i, j) == (k, l):
            print(i, j)
