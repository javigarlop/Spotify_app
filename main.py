import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging
from datetime import datetime
import json

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load secrets from secrets.json
with open('secrets.json') as f:
    secrets = json.load(f)

MY_CLIENT_ID = secrets['MY_CLIENT_ID']
MY_CLIENT_SECRET = secrets['MY_CLIENT_SECRET']

def get_bearer_token(client_id, client_secret):
    logging.info("Requesting bearer token...")
    response = requests.post('https://accounts.spotify.com/api/token', {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    })
    response_data = response.json()
    token = f"{response_data['token_type']} {response_data['access_token']}"
    logging.info("Bearer token obtained.")
    return token

def save_json(data, save_path, filename):
    os.makedirs(save_path, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_path_with_timestamp = os.path.join(save_path, f"{filename}_{timestamp}.json")

    with open(json_path_with_timestamp, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    logging.info(f"Data saved to {json_path_with_timestamp}")

def search_artist(artist, bearer_token, save_path):
    logging.info(f"Searching for artist: {artist}")
    endpoint = 'https://api.spotify.com/v1/search'
    url = f"{endpoint}?q={artist.replace(' ', '%20')}&type=artist&limit=10"
    response = requests.get(url, headers={'Authorization': bearer_token})
    items = response.json()['artists']['items']
    artist_data = [{'id': item['id'], 'name': item['name']} for item in items]
    df_artists = pd.DataFrame(artist_data)
    logging.info(f"Found {len(df_artists)} artists matching '{artist}'.")

    save_json(df_artists.to_dict(orient='records'), save_path, 'search_artist')

    return df_artists

def get_album_data(artist_id, bearer_token, save_path, limit=35):
    logging.info(f"Fetching albums for artist ID: {artist_id}")
    endpoint = f'https://api.spotify.com/v1/artists/{artist_id}/albums?limit=50'
    albums = []
    while endpoint and len(albums) < limit:
        response = requests.get(endpoint, headers={'Authorization': bearer_token})
        album_items = response.json()['items']
        albums.extend([{'name': album['name'], 'id': album['id']} for album in album_items])
        if len(albums) >= limit:
            break
        endpoint = response.json().get('next')
    albums = albums[:limit]
    logging.info(f"Found {len(albums)} albums for artist ID: {artist_id}")

    save_json(albums, save_path, 'get_album_data')

    return pd.DataFrame(albums)

def get_tracks_data(album_db, bearer_token, save_path):
    logging.info("Fetching tracks for each album...")
    all_tracks = []
    for idx, album in album_db.iterrows():
        logging.info(f"Fetching tracks for album: {album['name']} (ID: {album['id']})")
        endpoint = f'https://api.spotify.com/v1/albums/{album["id"]}/tracks'
        while endpoint:
            response = requests.get(endpoint, headers={'Authorization': bearer_token})
            track_items = response.json()['items']
            tracks = [{'album_name': album['name'], 'album_id': album['id'], 'track_name': track['name'], 'track_id': track['id']} for track in track_items]
            all_tracks.extend(tracks)
            endpoint = response.json().get('next')
    logging.info(f"Collected {len(all_tracks)} tracks from albums.")

    save_json(all_tracks, save_path, 'get_tracks_data')

    return pd.DataFrame(all_tracks)

def get_audio_features(tracks_db, bearer_token, save_path):
    logging.info("Fetching audio features for each track...")
    for idx, row in tracks_db.iterrows():
        endpoint = f'https://api.spotify.com/v1/audio-features/{row["track_id"]}'
        response = requests.get(endpoint, headers={'Authorization': bearer_token})
        features = response.json()
        tracks_db.at[idx, 'valence'] = features.get('valence')
        tracks_db.at[idx, 'energy'] = features.get('energy')
        logging.info(f"Processed track {idx + 1}/{len(tracks_db)}: {row['track_name']}")
    logging.info("Audio features fetched for all tracks.")

    save_json(tracks_db.to_dict(orient='records'), save_path, 'get_audio_features')

    return tracks_db

def plot_energy(tracks_db, save_path):
    logging.info("Plotting data...")
    plt.figure(figsize=(10, 8))
    sns.scatterplot(data=tracks_db, x='valence', y='energy', hue='album_id', legend=False)
    plt.title('Valence vs Energy')
    plt.xlabel('Valence')
    plt.ylabel('Energy')
    plt.text(0, 1, 'Turbulent/Angry', ha='left', va='top')
    plt.text(1, 1, 'Happy/Joyful', ha='right', va='top')
    plt.text(0, 0, 'Sad/Depressing', ha='left', va='bottom')
    plt.text(1, 0, 'Chill/Peaceful', ha='right', va='bottom')
    plt.axhline(0.5, color='gray', linestyle='--')
    plt.axvline(0.5, color='gray', linestyle='--')
    plt.xlim(0, 1)
    plt.ylim(0, 1)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_path_with_timestamp = f"{save_path}_{timestamp}.png"
    plt.savefig(save_path_with_timestamp)

    logging.info(f"Plot saved to {save_path_with_timestamp}")
    plt.close()  # Close the plot

def main(artist_name, save_path):
    os.makedirs(save_path, exist_ok=True)
    bearer_token = get_bearer_token(MY_CLIENT_ID, MY_CLIENT_SECRET)
    artist = search_artist(artist_name, bearer_token, save_path)
    if artist.empty:
        logging.error("No artist found")
        return

    artist_id = artist.iloc[0]['id']
    album_db = get_album_data(artist_id, bearer_token, save_path, limit=35)
    tracks_db = get_tracks_data(album_db, bearer_token, save_path)
    tracks_db = get_audio_features(tracks_db, bearer_token, save_path)

    plot_energy(tracks_db, save_path)

if __name__ == "__main__":
    save_path = "results_dir"
    os.makedirs(save_path, exist_ok=True)
    main('KAROL G', save_path)