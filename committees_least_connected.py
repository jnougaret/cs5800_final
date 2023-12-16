import pandas as pd
import networkx as nx
import itertools

def calculate_path_details(G, committee1, committee2):
    try:
        path = nx.shortest_path(G, committee1, committee2, weight='weight')
        path_cost = sum(G[path[i]][path[i + 1]]['weight'] for i in range(len(path) - 1))
        degree_of_separation = len(path) - 1  # Number of edges in the path
        return path_cost, degree_of_separation
    except nx.NetworkXNoPath:
        return float('inf'), None

def find_least_connected_committees():
    # Load the datasets
    edges_df = pd.read_csv('committee_edges.csv')
    committee_mapping_df = pd.read_csv('committee_mapping.csv')

    # Convert the committee mapping to a dictionary
    committee_names = committee_mapping_df.set_index('committee_id')['committee_name'].to_dict()

    # Create a graph
    G = nx.Graph()

    # Add edges to the graph using actual weights
    for _, row in edges_df.iterrows():
        G.add_edge(row['Committee1'], row['Committee2'], weight=row['CommonContributors'])

    # Calculate path costs and degrees of separation for all committee pairs
    committee_pairs = list(itertools.combinations(G.nodes(), 2))
    path_details = [(pair[0], pair[1], *calculate_path_details(G, pair[0], pair[1])) for pair in committee_pairs]

    # Sort by highest degree of separation and then by lowest path cost
    path_details.sort(key=lambda x: (-x[3], x[2]))
    top_least_connected = path_details[:10]

    # Convert committee IDs to names and display the results
    results = [(committee_names.get(pair[0]), committee_names.get(pair[1]), pair[2], pair[3]) for pair in top_least_connected]
    return results

top_least_connected = find_least_connected_committees()
for pair in top_least_connected:
    print(f"Committees: {pair[0]} and {pair[1]}, Total Path Cost: {pair[2]}, Degree of Separation: {pair[3]}")
