import pandas as pd
import networkx as nx
import random
import contributor_data as cd

def find_shortest_path(contributor_id1, contributor_id2, edges_df, contributor_names):
    # Create a graph
    G = nx.Graph()

    # Add edges to the graph
    G.add_edges_from([(row['Contributor1'], row['Contributor2']) for idx, row in edges_df.iterrows()])

    # Run Dijkstra's algorithm
    if contributor_id1 not in G or contributor_id2 not in G:
        return "One or both contributors not found in the network.", []

    try:
        path = nx.dijkstra_path(G, contributor_id1, contributor_id2)
    except nx.NetworkXNoPath:
        return "No path found", []

    # Map the contributor IDs to names
    path_names = [contributor_names.get(contributor_id, contributor_id) for contributor_id in path]

    return path, path_names

# Load the dataset
edges_df, contributor_names, _ = cd.export_network_data(0, 0)

# Select two random contributors and find the shortest path
contributor_mapping_df = pd.read_csv('contributor_mapping.csv')
random_contributors = random.sample(list(contributor_mapping_df['contributor_id']), 2)
path, path_names = find_shortest_path(random_contributors[0], random_contributors[1], edges_df, contributor_names)

print("Random Contributors:", random_contributors)
print("Path:", path)
print("Contributor Names:", path_names)
