import pandas as pd

# Load the dataset
df = pd.read_csv('2022_records.csv')

# Calculate total contributions made by each contributor
total_contributions_by_contributor = df.groupby('contributor_id')['amount'].sum()

# Extract unique contributors
unique_contributors = df['contributor_id'].unique()

# Precompute the recipient sets for each contributor
recipient_sets = {contributor: set(df[df['contributor_id'] == contributor]['recipient_id']) 
                  for contributor in unique_contributors}

# Initialize a dictionary to store edges and their weights
edges = {}

# Set a threshold for the minimum number of common recipients
threshold = 20

# Iterate over each unique pair of contributors
for i in range(len(unique_contributors)):
    for j in range(i+1, len(unique_contributors)):
        # Find the common recipients using precomputed sets
        common_recipients = recipient_sets[unique_contributors[i]].intersection(recipient_sets[unique_contributors[j]])

        # Check if the number of common recipients meets the threshold
        if len(common_recipients) >= threshold:
            edge = (unique_contributors[i], unique_contributors[j])
            edges[edge] = len(common_recipients)

# Convert the edges dictionary to a DataFrame
edges_df = pd.DataFrame([(k[0], k[1], v) for k, v in edges.items()], columns=['Contributor1', 'Contributor2', 'Weight'])

contributor_names = df.set_index('contributor_id')['contributor'].to_dict()

# Map each contributor to their total contribution amount
contributor_contribution_amounts = total_contributions_by_contributor.to_dict()
