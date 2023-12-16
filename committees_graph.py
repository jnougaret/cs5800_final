import plotly.graph_objects as go
import networkx as nx
import committee_data as cd

# Import the network edges and associated data
edges_df, committee_names, total_contributions = cd.export_network_data(1000000, 50)

# Create a graph using NetworkX
G = nx.Graph()
for _, row in edges_df.iterrows():
    G.add_edge(row['Committee1'], row['Committee2'], weight=row['CommonContributors'])

# Compute the positions of the nodes using a layout algorithm
pos = nx.spiral_layout(G)

# Prepare data for Plotly
edge_trace = go.Scatter(
    x=[],
    y=[],
    line=dict(width=0.5, color='#888'),
    hoverinfo='none',
    mode='lines')

for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_trace['x'] += tuple([x0, x1, None])
    edge_trace['y'] += tuple([y0, y1, None])

node_trace = go.Scatter(
    x=[],
    y=[],
    text=[committee_names[node] for node in G.nodes],
    hoverinfo='text',
    mode='markers',
    marker=dict(
        size=5, 
        line_width=2))

for node in G.nodes():
    x, y = pos[node]
    node_trace['x'] += tuple([x])
    node_trace['y'] += tuple([y])

# Create a figure and add traces for edges and nodes
fig = go.Figure(data=[edge_trace, node_trace],
             layout=go.Layout(
                title='<br>Network graph of committees',
                titlefont_size=16,
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                annotations=[ dict(
                    text="Python code: Network Graph using Plotly",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002 ) ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )

fig.show()
