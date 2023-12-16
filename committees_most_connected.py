import pandas as pd

def most_connected_committees(edges_csv='committee_edges.csv', combined_data_csv='combined_data.csv', committee_mapping_csv='committee_mapping.csv'):
    # Load the datasets
    edges_df = pd.read_csv(edges_csv)
    combined_data_df = pd.read_csv(combined_data_csv)
    committee_mapping_df = pd.read_csv(committee_mapping_csv)

    # Convert the committee mapping to a dictionary
    committee_names = committee_mapping_df.set_index('committee_id')['committee_name'].to_dict()

    # Sort edges by weight (common contributors) in descending order
    sorted_edges = edges_df.sort_values(by='CommonContributors', ascending=False).head(10)

    # Create a list to store the top most connected committee pairs and their common contribution amounts
    most_connected = []
    for _, edge in sorted_edges.iterrows():
        committee1, committee2 = edge['Committee1'], edge['Committee2']

        # Map committee IDs to names
        committee1_name = committee_names.get(committee1, "Unknown Committee")
        committee2_name = committee_names.get(committee2, "Unknown Committee")

        # Get contributions for each committee
        contributions1 = combined_data_df[combined_data_df['committee_id'] == committee1].groupby('contributor_id')['contribution_receipt_amount'].sum()
        contributions2 = combined_data_df[combined_data_df['committee_id'] == committee2].groupby('contributor_id')['contribution_receipt_amount'].sum()

        # Calculate the sum of minimum contributions from common contributors
        common_contributors = contributions1.index.intersection(contributions2.index)
        sum_min_contributions = sum(min(contributions1[contributor], contributions2[contributor]) for contributor in common_contributors)

        # Add the result to the list
        most_connected.append((committee1_name, committee2_name, sum_min_contributions))

    return most_connected

top_most_connected = most_connected_committees()
for pair in top_most_connected:
    print(f"Committees: {pair[0]} and {pair[1]}, Common Contribution Amount: {pair[2]}")
