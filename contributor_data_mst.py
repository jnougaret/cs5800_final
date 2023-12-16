import pandas as pd
import networkx as nx

def export_network_data_mst(min_contribution_amount, edge_threshold):
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

    # Create a graph
    G = nx.Graph()

    # Iterate over each unique committee
    for committee, contributors in committee_to_contributors.items():
        for contributor1 in contributors:
            for contributor2 in contributors:
                if contributor1 != contributor2:
                    edge = tuple(sorted([contributor1, contributor2]))
                    if G.has_edge(*edge):
                        G[edge[0]][edge[1]]['weight'] += 1
                    else:
                        G.add_edge(*edge, weight=1)

    # Filter edges below the threshold
    G_filtered = nx.Graph()
    for u, v, data in G.edges(data=True):
        if data['weight'] >= edge_threshold:
            G_filtered.add_edge(u, v, weight=data['weight'])

    # Compute the Minimum Spanning Tree
    mst = nx.minimum_spanning_tree(G_filtered)

    # Convert MST edges to a DataFrame
    mst_edges = pd.DataFrame(mst.edges(data=True), columns=['Contributor1', 'Contributor2', 'Data'])
    mst_edges['Weight'] = mst_edges['Data'].apply(lambda x: x['weight'])
    mst_edges.drop('Data', axis=1, inplace=True)

    # Map contributor_id to contributor_name
    contributor_names = contributor_mapping.set_index('contributor_id')['contributor_name'].to_dict()

    # Export the MST edges DataFrame
    mst_edges.to_csv('mst_contributor_edges.csv', index=False)

    # Return the MST edges DataFrame along with contributor names and total contributions
    return mst_edges, contributor_names, total_contributions.to_dict()
