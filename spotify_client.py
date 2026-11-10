import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyException

def initialise_spotipy():
    """Initialise the Spotipy client with the required scope."""
    scope = 'user-read-currently-playing'

    try:
        sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(scope=scope)
        )
        return sp

    except SpotifyException as e:
        print(f"[SPOTIFY ERROR] Spotify API error during initialisation: {e}")
        return None

    except Exception as e:
        print(f"[SPOTIFY ERROR] Unexpected error during initialisation: {e}")
        return None

    
def get_current_track_info(sp):

   
    try:
        current_track = sp.current_user_playing_track()

        # Check that Spotify returned a track
        if current_track and current_track.get('item'):
            item = current_track['item']

            # Check that artwork exists
            images = item.get('album', {}).get('images', [])
            artwork_url = images[0]['url'] if images else None

            # Check that an artist exists
            artists = item.get('artists', [])
            artist_name = artists[0]['name'] if artists else "Unknown Artist"

            # Build track dictionary
            track_dict = {
                "track_id": item.get('id'),
                "title": item.get('name'),
                "artist": artist_name,
                "album": item.get('album', {}).get('name'),
                "artwork_url": artwork_url,
                "is_playing": current_track.get('is_playing'),
                "progress_ms": current_track.get('progress_ms'),
                "duration_ms": item.get('duration_ms')
            }

            # Return dictionary to main.py
            return track_dict

        else:
            print("[SPOTIFY] No track is currently playing.")
            return None

    except SpotifyException as e:
        print(f"[SPOTIFY ERROR] Spotify API error: {e}")
        return None

    except Exception as e:
        print(f"[SPOTIFY ERROR] Unexpected error: {e}")
        return None

if __name__ == "__main__":

    print("Checking Spotify connection...")

    sp = initialise_spotipy()

    if sp is None:
        print("Spotify initialisation failed.")

    else:
        track_info = get_current_track_info(sp)

        if track_info:
            print("Track detected!")
            print(track_info)

        else:
            print("No track information returned.")

# type: ignore