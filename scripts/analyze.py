# %%
import pandas as pd
import glob

# %%
dates = ["2025-05-23", "2025-05-29", "2025-05-30", "2025-05-31", "2025-06-06","2025-06-08", "2025-06-10"]

# %% [markdown]
# ## ParMed

# %%
parmed_columns = [
    'itemId', 'ndc', 'price',
    'description', 'manufacturer', 'strength'
    ]
tables = []
for date in dates:
    print(f"./data/parmed-{date}.csv")
    df = pd.read_csv(f"./data/parmed-{date}.csv")
    # df = df[df['itemId'].isin(item_numbers)]
    print(df.shape)
    df = df[parmed_columns]
    df['date'] = date
    tables.append(df)

df_parmed = pd.concat(tables)

# %%
df_parmed_describe = df_parmed.groupby('itemId')['price'].describe()
df_parmed_describe['delta'] = df_parmed_describe['max'] - df_parmed_describe['min']
df_parmed_describe = df_parmed_describe.sort_values('delta', ascending=False)

# %%
df_parmed = df_parmed_describe.merge(df_parmed.drop_duplicates(subset=['itemId']), how ='left', left_index=True, right_on='itemId')

# %%
df_parmed = df_parmed.drop(columns=['date'])
df_parmed.to_csv('./data/parmed_deltas.csv', index=False)

# %% [markdown]
# ## BluPax

# %%
blupax_columns = [
    'id', 'wac', 'awp', 'ndc_formatted', 'price', 'unit_price',
    'description', 'product_size', 'manufacturer_name', 'brand', 'strength'
    ]
tables = []
for date in dates:
    print(f"./data/blupax-{date}.csv")
    df = pd.read_csv(f"./data/blupax-{date}.csv")
    print(df.shape)
    df = df[blupax_columns]
    df['date'] = date
    tables.append(df)

df_blupax = pd.concat(tables)

# %%
df_blupax_describe = df_blupax.groupby('id')['price'].describe()
df_blupax_describe['delta'] = df_blupax_describe['max'] - df_blupax_describe['min']
df_blupax_describe = df_blupax_describe.sort_values('delta', ascending=False)

# %%
df_blupax = df_blupax_describe.merge(df_blupax.drop_duplicates(subset=['id']), how ='left', left_index=True, right_on='id')

# %%
df_blupax = df_blupax.drop(columns=['date'])
df_blupax.to_csv('./data/blupax_delta.csv', index=False)


