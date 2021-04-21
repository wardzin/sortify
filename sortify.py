import spotipy
import spotipy.util
import numpy as np
import pandas as pd
from tqdm.autonotebook import tqdm, trange


client_id = 'b69a9985fa8842deb0691b2d0e3f0b69'
client_secret = 'd9e9ae2924174c139a5a9ccb303f9f3a'
redirect_uri = 'http://localhost/'

username = '22mrmbu7oumkrb56tcsclawdi' # Daniel

token = spotipy.util.prompt_for_user_token(username, 'user-library-read playlist-modify-private', client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
sp = spotipy.Spotify(auth=token)


def chunks(n, x):
    return [x[i:i + n] for i in range(0, len(x), n)]


def get_user_tracks():
    tracks = []

    offset = 0
    pbar = tqdm()
    while True:
        track_set = sp.current_user_saved_tracks(limit=50, offset=offset)
        if track_set:
            track_set = track_set['items']
            pbar.update(len(track_set))
            tracks += track_set
            if len(track_set) < 50:
                pbar.close()
                break
        else:
            pbar.close()
            break
        offset += 50

    track_data = {
        'id': [],
        'name': [],
        'artist': [],
    }
    for track in tracks:
        if 'track' not in track:
            continue
        track = track['track']
        track_data['id'].append(track['id'])
        track_data['name'].append(track['name'])
        if 'remix' in track['name'].lower():
            track_data['artist'].append(track['artists'][-1]['id'])
        else:
            track_data['artist'].append(track['artists'][0]['id'])

    return pd.DataFrame(track_data).set_index('id')


def get_track_features(tracks):
    feature_data = {
        'id': [],
        'danceability': [],
        'energy': [],
        'key': [],
        'loudness': [],
        'mode': [],
        'speechiness': [],
        'acousticness': [],
        'instrumentalness': [],
        'liveness': [],
        'valence': [],
        'tempo': [],
        'time_signature': [],
    }

    for chunk in tqdm(chunks(50, tracks)):
        track_set = sp.audio_features(chunk)
        for track_features in track_set:
            for key in feature_data.keys():
                feature_data[key].append(track_features[key])

    return pd.DataFrame(feature_data).set_index('id')


def get_timbre_data(tracks):
    timbre_data = []

    for track in tqdm(tracks):
        timbres = []
        durations = []
        for segment in sp.audio_analysis(track)['segments']:
            timbres.append(segment['timbre'])
            durations.append(segment['duration'])
        timbre_data.append(np.average(timbres, axis=0, weights=durations))
        
    return pd.DataFrame(timbre_data, index=tracks)


def get_artist_data(artists):
    artist_data = {
        'id': [],
        'name': [],
        'popularity': [],
        'genres': []
    }

    for chunk in tqdm(chunks(50, artists)):
        for artist in sp.artists(chunk)['artists']:
            artist_data['id'].append(artist['id'])
            artist_data['name'].append(artist['name'])
            artist_data['popularity'].append(artist['popularity'])
            artist_data['genres'].append(artist['genres'])

    return pd.DataFrame(artist_data).set_index('id')


def get_related_artists(artists):
    related_artists = {}

    for artist in tqdm(artists):
        related_artist_list = sp.artist_related_artists(artist)['artists']

        if len(related_artist_list) <= 1:
            continue

        related_artists[artist] = []
        for related_artist in related_artist_list:
            related_artists[artist].append(related_artist['id'])

    return related_artists
