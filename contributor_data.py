import pandas as pd

def export_network_data(min_contribution_amount, edge_threshold):
    # Load the datasets
    df = pd.read_csv('combined_data.csv')
    contributor_mapping = pd.read_csv('contributor_mapping.csv')

    # Calculate total contributions for each contributor
    total_contributions = df.groupby('contributor_id')['contribution_receipt_amount'].sum()

    # Filter based on the minimum contribution amount
    filtered_contributors = total_contributions[total_contributions >= min_contribution_amount].index

    # Filter the main DataFrame to include only the filtered contributors
    df_filtered = df[df['contributor_id'].isin(filtered_contributors)]

    # Map committees to contributors
    committee_to_contributors = df_filtered.groupby('committee_id')['contributor_id'].apply(set).to_dict()

    # Prepare data for contributor Nodes network graph
    edges = {}

    # Iterate over each unique committee
    for committee, contributors in committee_to_contributors.items():
        # Iterate over each unique pair of contributors in this committee
        for contributor1 in contributors:
            for contributor2 in contributors:
                if contributor1 != contributor2:
                    edge = tuple(sorted([contributor1, contributor2]))
                    edges[edge] = edges.get(edge, 0) + 1

    # Filter edges based on threshold
    filtered_edges = {k: v for k, v in edges.items() if v >= edge_threshold}

    # Convert the edges dictionary to a DataFrame
    edges_df = pd.DataFrame([(k[0], k[1], v) for k, v in filtered_edges.items()], 
                            columns=['Contributor1', 'Contributor2', 'Weight'])

    # Map contributor_id to contributor_name
    contributor_names = contributor_mapping.set_index('contributor_id')['contributor_name'].to_dict()

    # Export the edges DataFrame
    edges_df.to_csv('contributor_edges.csv', index=False)

    # Return the edges DataFrame along with contributor names and total contributions
    return edges_df, contributor_names, total_contributions.to_dict()

export_network_data(0, 0)