# %%
import json
import pandas as pd

dir_path = "experiments/matching/"

df_parmed = pd.read_csv(dir_path + "unique_parmed_samples.csv")
df_blupax = pd.read_csv(dir_path + "unique_blupax_samples.csv")
df_report = pd.read_csv(dir_path + "product-report-top-1000-with-predictions.csv", low_memory=False)
print(df_parmed.shape)
print(df_blupax.shape)
print(df_report.shape)

# %%
df_report = df_report[df_report['brand_status'] == 'Generic'].reset_index(drop=True)
columns = [
    'ABC #', 'NDC', 'Product Description', 'Primary Ingredient HIC4 Desc', 'Supplier Name', 'Current Acq Cost', 
    'Price Per Dose', 'FDB Package Size Qty', 'Unit Size Qty', 'Route Desc', 'Contract Name', 'Contract Cost', 'brand_status'
    ]
df_report = df_report[columns]
print(df_report.shape)

# %%
df_blupax['text'] = df_blupax.apply(lambda x: x.to_json().lower().replace('-', ' '), axis=1)
df_parmed['text'] = df_parmed.apply(lambda x: x.to_json().lower().replace('-', ' '), axis=1)
texts_blupax = list(df_blupax['text'].values)
texts_parmed = list(df_parmed['text'].values)

# %%
df_report['found_blupax'] = False
df_report['found_parmed'] = False
df_report['index_blupax'] = None
df_report['index_parmed'] = None
df_report['counter_blupax'] = 0
df_report['counter_parmed'] = 0


for idx, row in df_report.iterrows():
    keyword_1 = row['Primary Ingredient HIC4 Desc'].split(' ')[0].lower()
    if len(keyword_1) <= 3:
        keyword_1_list = row['Primary Ingredient HIC4 Desc'].split(' ')
        keyword_1 = keyword_1_list[1].lower() + ' ' + keyword_1_list[2].lower()
    keyword_2 = row['Product Description'].split(' ')[0].lower()
    if len(keyword_2) <= 3:
        keyword_2_list = row['Product Description'].split(' ')
        keyword_2 = keyword_2_list[1].lower() + ' ' + keyword_2_list[2].lower()

    indices_blupax = []
    for i, text in enumerate(texts_blupax):
        if keyword_1 in text or keyword_2 in text:
            indices_blupax.append(i)
    if len(indices_blupax) > 0:
        df_report.loc[idx, 'found_blupax'] = True
        df_report.loc[idx, 'index_blupax'] = json.dumps(indices_blupax)
        df_report.loc[idx, 'counter_blupax'] = len(indices_blupax)

    indices_parmed = []
    for i, text in enumerate(texts_parmed):
        if keyword_1 in text or keyword_2 in text:
            indices_parmed.append(i)
    if len(indices_parmed) > 0:
        df_report.loc[idx, 'found_parmed'] = True
        df_report.loc[idx, 'index_parmed'] = json.dumps(indices_parmed)
        df_report.loc[idx, 'counter_parmed'] = len(indices_parmed)


print(df_report[['found_parmed', 'found_blupax']].value_counts())

# %%
df_report.to_csv(dir_path + "product-report-top-1000-processed.csv", index=False)
