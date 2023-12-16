import pandas as pd
from fuzzywuzzy import process

# Load the dataset
df = pd.read_csv('schedule_a-2023-12-14T10_42_51.csv', low_memory=False)

# Filter the DataFrame to include only entries with "election_type" as "G2022"
df_filtered = df[df['election_type'] == 'G2022']

# Selecting the specified columns
selected_columns = ['committee_id', 
                    'committee_name', 
                    'contributor_id', 
                    'contributor_name',
                    'contribution_receipt_amount']
df_selected = df_filtered[selected_columns].copy()

# Function to create a mapping table using fuzzy matching
def create_mapping_table(df, id_col, name_col):
    # Creating a dictionary to store the mapping
    mapping = {}

    # Unique identifiers
    unique_ids = df[id_col].unique()

    for uid in unique_ids:
        # All names associated with this id
        names = df[df[id_col] == uid][name_col].unique()

        # Fuzzy matching to find the most common name
        if len(names) > 0:
            most_common_name, _ = process.extractOne(uid, names)
            mapping[uid] = most_common_name

    return pd.DataFrame(list(mapping.items()), columns=[id_col, name_col])

# Create mapping tables
committee_mapping = create_mapping_table(df_selected, 'committee_id', 'committee_name')
contributor_mapping = create_mapping_table(df_selected, 'contributor_id', 'contributor_name')

# Remove name columns from the main DataFrame
df_selected.drop(['committee_name', 'contributor_name'], axis=1, inplace=True)

# Group by 'committee_id' and 'contributor_id' and sum 'contribution_receipt_amount'
combined_df = df_selected.groupby(['committee_id', 'contributor_id']).agg({
    'contribution_receipt_amount': 'sum'
}).reset_index()

# Remove records where 'contribution_receipt_amount' is insignificant
combined_df = combined_df[combined_df['contribution_receipt_amount'] >= 500]

# Export the combined DataFrame
combined_df.to_csv('combined_data.csv', index=False)

# Export the committee mapping
committee_mapping.to_csv('committee_mapping.csv', index=False)

# Export the contributor mapping
contributor_mapping.to_csv('contributor_mapping.csv', index=False)
