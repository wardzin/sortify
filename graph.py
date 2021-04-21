import networkx as nx


def initialize_graph(initial_artists):
    G = nx.Graph()

    for artist in initial_artists:
        G.add_node(artist)
        G.nodes[artist]['fetched'] = False
        G.nodes[artist]['depth'] = 0

    return G


def populate_related_artists(G, max_depth=2):
    base_artists = []

    for artist, node in G.nodes.data():
        if node['depth'] == 0:
            base_artists.append(artist)

    estimated_total = len(base_artists) * 20**max_depth

    with tqdm(total=estimated_total) as pbar:
        def fetch_related_artists(artist, depth=0):
            if depth != 0:
                pbar.update()
            if depth == max_depth:
                return

            if G.nodes[artist]['fetched']:
                for related_artist in G[artist]:
                    fetch_related_artists(related_artist, depth=depth+1)
            else:
                related_artists = sp.artist_related_artists(artist_id)['artists']
                



    

            



    
