import pandas as pd
import networkx as nx

# Read the CSV data
df = pd.read_csv('theoretical_twitch_view_data.csv')

# Create a directed graph
G = nx.DiGraph()

# Add nodes and edges
for _, row in df.iterrows():
    viewer = row['viewer']
    streamer = row['streamer']
    watch_time = row['watch_time']
    
    # Add nodes if they don't exist
    if not G.has_node(viewer):
        G.add_node(viewer, type='viewer')
    if not G.has_node(streamer):
        G.add_node(streamer, type='streamer')
    
    # Add edge with weight
    G.add_edge(viewer, streamer, weight=watch_time)

# Calculate node attributes
# For streamers: number of unique viewers
streamer_viewer_counts = {}
for streamer in [n for n, d in G.nodes(data=True) if d['type'] == 'streamer']:
    streamer_viewer_counts[streamer] = len([n for n in G.predecessors(streamer)])

# For viewers: total watch time
viewer_watch_times = {}
for viewer in [n for n, d in G.nodes(data=True) if d['type'] == 'viewer']:
    viewer_watch_times[viewer] = sum(d['weight'] for _, _, d in G.edges(viewer, data=True))

# Add attributes to nodes
nx.set_node_attributes(G, streamer_viewer_counts, 'viewer_count')
nx.set_node_attributes(G, viewer_watch_times, 'total_watch_time')

# Export to GEXF format
nx.write_gexf(G, 'twitch_network.gexf') 