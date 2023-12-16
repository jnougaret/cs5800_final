import pandas as pd

def export_network_data(min_contribution_amount, edge_threshold):
    # Load the datasets
    df = pd.read_csv('combined_data.csv')
    committee_mapping = pd.read_csv('committee_mapping.csv')

    # Calculate total contributions for each committee
    total_contributions = df.groupby('committee_id')['contribution_receipt_amount'].sum()

    # Convert the total_contributions dictionary to a DataFrame
    total_contributions_df = pd.DataFrame(list(total_contributions.items()), columns=['committee_id', 'total_contribution_amount'])

    # Export the DataFrame to CSV
    total_contributions_df.to_csv('total_contributions.csv', index=False)

    # Filter based on the minimum contribution amount
    filtered_committees = total_contributions[total_contributions >= min_contribution_amount].index

    # Filter the main DataFrame to include only the filtered committees
    df_filtered = df[df['committee_id'].isin(filtered_committees)]

    # Prepare data for Committee Nodes network graph
    unique_committees = df_filtered['committee_id'].unique()
    edges = {}

    # Iterate over each unique pair of committees
    for i in range(len(unique_committees)):
        for j in range(i+1, len(unique_committees)):
            contributors_i = set(df_filtered[df_filtered['committee_id'] == unique_committees[i]]['contributor_id'])
            contributors_j = set(df_filtered[df_filtered['committee_id'] == unique_committees[j]]['contributor_id'])
            common_contributors = contributors_i.intersection(contributors_j)

            for contributor in common_contributors:
                edge = (unique_committees[i], unique_committees[j])
                edges[edge] = edges.get(edge, 0) + 1

    # Convert the edges dictionary to a DataFrame
    edges_df = pd.DataFrame([(k[0], k[1], v) for k, v in edges.items() if v >= edge_threshold], 
                            columns=['Committee1', 'Committee2', 'CommonContributors'])

    # Map committee_id to committee_name
    committee_names = committee_mapping.set_index('committee_id')['committee_name'].to_dict()

    # Export the edges DataFrame
    edges_df.to_csv('committee_edges.csv', index=False)

    # Return the edges DataFrame along with committee names and total contributions
    return edges_df, committee_names, total_contributions.to_dict()
