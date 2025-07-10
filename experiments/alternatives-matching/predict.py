import json
import dotenv
import pandas as pd

from openai import OpenAI


dotenv.load_dotenv()

client = OpenAI()
dir_path = "experiments/alternatives-matching/"

df = pd.read_csv(dir_path + "product-report-top-1000-preprocessed.csv")
output_file = dir_path + "product-report-top-1000-alternative-predictions.csv"

df_parmed = pd.read_csv(dir_path + "unique_parmed_samples.csv")
df_blupax = pd.read_csv(dir_path + "unique_blupax_samples.csv")

df_parmed['text'] = df_parmed.apply(lambda x: x.to_json().lower(), axis=1)
texts_parmed = list(df_parmed['text'].values)
df_blupax['text'] = df_blupax.apply(lambda x: x.to_json().lower(), axis=1)
texts_blupax = list(df_blupax['text'].values)

df['alternatives_parmed'] = None
df['alternative_index_parmed'] = None
df['alternative_reasoning_parmed'] = None
df['alternative_price_parmed'] = None
df['alternative_description_parmed'] = None

df['alternatives_blupax'] = None
df['alternative_index_blupax'] = None
df['alternative_reasoning_blupax'] = None
df['alternative_price_blupax'] = None
df['alternative_description_blupax'] = None

for idx, row in df.iterrows():
    print(idx)
    source = row[['Product Description', 'Primary Ingredient HIC4 Desc', 'Supplier Name', 'Route Desc']].to_json()
    print('Source:\n', source)

    if row['found_parmed']:
        indices = json.loads(row['index_parmed'])
        alternatives = list(df_parmed.iloc[indices]['text'].values)
        alternatives = [{'index': k, 'drug': alternative} for k, alternative in enumerate(alternatives)]
        print('Alternatives (Parmed):\n', alternatives)
        alternatives = json.dumps(alternatives)
        df.at[idx, 'alternatives_parmed'] = alternatives

        response = client.responses.create(
            prompt={
                "id": "pmpt_686e6e307768819395b8d349ed4c12f10341e5bc38652685",
                "variables": {
                    "source": source,
                    "alternatives": alternatives,
                }
            }
        )
        response_data = json.loads(response.output_text)
        if 0 <= int(response_data['alternative_index']) <= len(indices) - 1:
            alternative_index = indices[int(response_data['alternative_index'])]
            df.at[idx, 'alternative_index_parmed'] = alternative_index
            df.at[idx, 'alternative_price_parmed'] = df_parmed.iloc[alternative_index]['Min Price']
            df.at[idx, 'alternative_description_parmed'] = df_parmed.iloc[alternative_index]['Description']
            print('Alternative found (Parmed):\n', df_parmed.iloc[alternative_index]['Description'])
        else:
            df.at[idx, 'alternative_index_parmed'] = -1

        df.at[idx, 'alternative_reasoning_parmed'] = response_data['reasoning']
        

    if row['found_blupax']:
        indices = json.loads(row['index_blupax'])
        alternatives = list(df_blupax.iloc[indices]['text'].values)
        alternatives = [{'index': k, 'drug': alternative} for k, alternative in enumerate(alternatives)]
        print('Alternatives (Blupax):\n', alternatives)
        alternatives = json.dumps(alternatives)
        df.at[idx, 'alternatives_blupax'] = alternatives

        response = client.responses.create(
            prompt={
                "id": "pmpt_686e6e307768819395b8d349ed4c12f10341e5bc38652685",
                "variables": {
                    "source": source,
                    "alternatives": alternatives,
                }
            }
        )
        response_data = json.loads(response.output_text)
        if 0 <= int(response_data['alternative_index']) <= len(indices) - 1:
            alternative_index = indices[int(response_data['alternative_index'])]
            df.at[idx, 'alternative_index_blupax'] = alternative_index
            df.at[idx, 'alternative_price_blupax'] = df_blupax.iloc[alternative_index]['Min Price']
            df.at[idx, 'alternative_description_blupax'] = df_blupax.iloc[alternative_index]['Description']
            print('Alternative found (Blupax):\n', df_blupax.iloc[alternative_index]['Description'])
        else:
            df.at[idx, 'alternative_index_blupax'] = -1

        df.at[idx, 'alternative_reasoning_blupax'] = response_data['reasoning']

    df.to_csv(output_file, index=False)
