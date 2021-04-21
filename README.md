# Sortify
Organizes your Spotify music library into playlists using machine learning.

### How It Works
1. The user authenticates to allow access to their Spotify library, and their saved tracks are fetched.
2. Using the Spotify API's [related-artists endpoint](https://developer.spotify.com/console/get-artist-related-artists/), a graph (network) of related artists is recursively built (up to a certain depth, I stopped at 200,000+ artists and 1,000,000+ connections).
3. We traverse the graph to figure out the shortest path length between the user's saved artists, which gives us a measure of artist similarity.
4. The artists are clustered using scikit-learn's [SpectralClustering](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.SpectralClustering.html).
5. Finally, we automatically save playlists based on the clustered artists and their tracks into their Spotify account. The playlists are named based on their most promiment genre (according to Spotify's genre labeling for the artists).

From the tests I ran, the playlist clustering is **very good**. While this is still a prototype, all of the above functionality is there, and exists inside the `related_artist_clustering.ipynb` notebook. 

The reason this hasn't been developed into a full-fledged web app yet is because of how computationally expensive it is. Good playlist clustering requires a very large graph of artists, which takes a long time to both build and find the shortest paths. I am currently exploring alternate avenues and workarounds for this fundamental problem.
