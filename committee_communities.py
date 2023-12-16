import networkx as nx
import community as community_louvain
import committee_data as cd

# Load dataset
edges_df, committee_names, _ = cd.export_network_data(0, 0)

# Graph Construction
G = nx.Graph()
for _, row in edges_df.iterrows():
    G.add_edge(row['Committee1'], row['Committee2'], weight=row['CommonContributors'])

# Apply Community Detection (Louvain)
partition = community_louvain.best_partition(G, weight='weight')

# Analyzing Results
# The partition is a dictionary mapping node to community
communities = {}
for node, comm_id in partition.items():
    # Translate node IDs to committee names for readability
    committee_name = committee_names.get(node, "Unknown Committee")
    communities.setdefault(comm_id, []).append(committee_name)

# Display the detected communities
print("Detected Communities:")
for comm_id, nodes in communities.items():
    print(f"\nCommunity {comm_id}:")
    for committee in nodes:
        print(committee)

# Get the set of all committees from the community detection results
communities_committees = set()
for _, nodes in communities.items():
    communities_committees.update(nodes)

# Get the set of all committees from committee_mapping
all_committees = set(committee_names.values())

# Find committees not in any community
outliers = all_committees - communities_committees

# Display the results
print("\nCommittees not in any community (Outliers):")
for committee in outliers:
    print(committee)
