import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os 

client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
redirect_url = os.getenv("SPOTIPY_REDIRECT_URI")

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="3075b3e61629474991ffd88efc4edf7c",
    client_secret="edf2b76f18c14a4c84441db29dac9985",
    redirect_uri= "http://localhost:8888/callback",
    scope="playlist-modify-private",
    show_dialog=True,
    username= "31ja3p6clwuyjzna4hpdbsm7oigm"
))

date = input("Which year you want to travel to?\nWrite the date in this format (YYYY-MM-DD): ")
print(date)

response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}")

soup = BeautifulSoup(response.text, "html.parser")
song_names_spans = soup.select("li ul li h3")  
song_names = [song.get_text().strip() for song in song_names_spans]

print("Top songs:")
for idx, song in enumerate(song_names):
    print(f"{idx + 1}. {song}")


user_id = sp.current_user()['id']
playlist = sp.user_playlist_create(user=user_id, name=f"Top Songs from {date}", public=False)


for song in song_names:
    results = sp.search(q=song, type='track', limit=1)
    tracks = results['tracks']['items']
    if tracks:
        track_uri = tracks[0]['uri']
        sp.playlist_add_items(playlist_id=playlist['id'], items=[track_uri])
        print(f"Added {song} to the playlist.")
    else:
        print(f"Couldn't find {song} on Spotify.")
