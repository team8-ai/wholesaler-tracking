import dotenv
import pandas as pd
import json
from openai import OpenAI

dotenv.load_dotenv()

client = OpenAI()

dir_path = "experiments/generic-classification/"
df = pd.read_csv(dir_path + 'product-report-full.csv')
output_file = dir_path + 'product-report-top-1000-with-predictions.csv'

print(df.shape)

# Add new columns to the dataframe
df['brand_status'] = None
df['generic_alternative_available'] = None
df['generic_manufacturers'] = None
df['reasoning'] = None

print(df.shape)

for index, row in df.iterrows():
    print(f"Processing row {index + 1}/{len(df)}: {row['Product Description']}")
    
    try:
        response = client.responses.create(
            prompt={
                "id": "pmpt_686a6cae5a5081939975224e71d812f10848a83d45ec9a02",
                "version": "4",
                "variables": {
                    "ndc": str(row['NDC']),
                    "ingredient": row['Primary Ingredient HIC4 Desc'],
                    "product": row['Product Description'],
                    "route": row['Route Desc']
                }
            }
        )
        
        # Parse the JSON response
        response_data = json.loads(response.output_text)
        
        # Populate the new columns
        df.at[index, 'brand_status'] = response_data.get('brand_status', '')
        df.at[index, 'generic_alternative_available'] = response_data.get('generic_alternative_available', '')
        df.at[index, 'generic_manufacturers'] = json.dumps(response_data.get('generic_manufacturers', []))
        df.at[index, 'reasoning'] = response_data.get('reasoning', '')
        
        print(f"  - Brand Status: {response_data.get('brand_status', 'N/A')}")
        print(f"  - Generic Available: {response_data.get('generic_alternative_available', 'N/A')}")
        
    except Exception as e:
        print(f"  - Error processing row {index + 1}: {str(e)}")
        # Set default values for failed rows
        df.at[index, 'brand_status'] = 'ERROR'
        df.at[index, 'generic_alternative_available'] = False
        df.at[index, 'generic_manufacturers'] = '[]'
        df.at[index, 'reasoning'] = f'Error: {str(e)}'

    # Save the updated dataframe
    df.to_csv(output_file, index=False)
    
    # Stop after 1000 rows
    if index >= 1000:
        break

print(f"\nProcessing complete! Results saved to {output_file}")
