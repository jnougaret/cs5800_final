import pandas as pd
import networkx as nx

def export_network_data_mst(min_contribution_amount, edge_threshold):
    # Load the datasets
    df = pd.read_csv('combined_data.csv')
    committee_mapping = pd.read_csv('committee_mapping.csv')

    # Calculate total contributions for each committee
    total_contributions = df.groupby('committee_id')['contribution_receipt_amount'].sum()

    # Filter based on the minimum contribution amount
    filtered_committees = total_contributions[total_contributions >= min_contribution_amount].index

    # Filter the main DataFrame to include only the filtered committees
    df_filtered = df[df['committee_id'].isin(filtered_committees)]

    # Create a graph
    G = nx.Graph()

    # Iterate over each unique pair of committees
    for i in range(len(filtered_committees)):
        contributors_i = set(df_filtered[df_filtered['committee_id'] == filtered_committees[i]]['contributor_id'])
        for j in range(i+1, len(filtered_committees)):
            contributors_j = set(df_filtered[df_filtered['committee_id'] == filtered_committees[j]]['contributor_id'])
            common_contributors = contributors_i.intersection(contributors_j)

            if len(common_contributors) >= edge_threshold:
                edge = (filtered_committees[i], filtered_committees[j])
                G.add_edge(*edge, weight=len(common_contributors))

    # Compute the Minimum Spanning Tree
    mst = nx.minimum_spanning_tree(G)

    # Convert MST edges to a DataFrame
    mst_edges = pd.DataFrame(mst.edges(data=True), columns=['Committee1', 'Committee2', 'Data'])
    mst_edges['CommonContributors'] = mst_edges['Data'].apply(lambda x: x['weight'])
    mst_edges.drop('Data', axis=1, inplace=True)

    # Map committee_id to committee_name
    committee_names = committee_mapping.set_index('committee_id')['committee_name'].to_dict()

    # Export the MST edges DataFrame
    mst_edges.to_csv('mst_committee_edges.csv', index=False)

    # Return the MST edges DataFrame along with committee names and total contributions
    return mst_edges, committee_names, total_contributions.to_dict()
