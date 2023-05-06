from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth

# scapping billboard 
date = input("Which year do you want to trave to? Type the date in this format YYYY-MM-DD ")
response = requests.get("https://www.billboard.com/charts/hot-100/"+date)
music_web = response.text
spotify_url = " https://api.spotify.com."
soup = BeautifulSoup(music_web, "html.parser")
song_names = soup.select("li ul li h3")
song_title = [song.getText().strip() for song in song_names]

# spotyfy authentication

Client_id = "2876d23fcdea483ba3b338c2b12f5c6b"
Client_secret = "2de9160f43984c8cb7cfe2708611a667"

spotify_response = requests.get(spotify_url)
spotify = spotify_response.json
# print(spotify)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://localhost:8080",        
        client_id=Client_id,
        client_secret=Client_secret,
        show_dialog=True,
        cache_path="token.txt"
    )
)

user_id = sp.current_user()['id']
print(user_id)

# searching spotify for songs by title
song_uris = []
year = date.split("-")[0]

for song in song_title:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        url = result["tracks"]["items"][0]['uri']
        song_uris.append(url)
    except IndexError:
        print(f"{song} does not exist in spotify. skipped.")

# creating a new private playelist in spotify
playlist = sp.user_playlist_create(user=user_id,
                                   name=f"{date} Billboard 100",
                                   public=False)
print(playlist)

# adding songs found into the new playlist
sp.playlist_add_items(playlist_id=playlist['id'],items=song_uris)