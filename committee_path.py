import pandas as pd
import networkx as nx
import random
import committee_data as cd

def find_shortest_path(committee_id1, committee_id2,):
    # Load the dataset
    edges_df, committee_names, total_contributions = cd.export_network_data(0, 0)

    # Create a graph
    G = nx.Graph()

    # Add edges to the graph
    for _, row in edges_df.iterrows():
        G.add_edge(row['Committee1'], row['Committee2'], weight=1)

    # Run Dijkstra's algorithm
    try:
        path = nx.dijkstra_path(G, committee_id1, committee_id2)
    except nx.NetworkXNoPath:
        return "No path found", []

    # Map the committee IDs to names
    path_names = [committee_names.get(committee_id, committee_id) for committee_id in path]

    return path, path_names

# Select two random committees and find the shortest path
committee_mapping_df = pd.read_csv('committee_mapping.csv')
random_committees = random.sample(list(committee_mapping_df['committee_id']), 2)
path, path_names = find_shortest_path(random_committees[0], random_committees[1])

print("Random Committees:", random_committees)
print("Path:", path)
print("Committee Names:", path_names)
