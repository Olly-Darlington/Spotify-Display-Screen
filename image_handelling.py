if __name__ == "__main__":

    import spotipy
    from spotipy.oauth2 import SpotifyOAuth

    scope = 'user-read-currently-playing'
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(scope='user-read-currently-playing'))

    current_track = sp.current_user_playing_track()

    # Ensure that a track is playing
    if current_track is not None:
    # Get the album art
       track_dict = {
           "artwork_url": current_track['item']['album']['images'][0]['url']
        }
       artwork_url = track_dict['artwork_url']
       print(f"Album art URL: {track_dict['artwork_url']}")
    else:
        print("No track is currently playing.")


def update_artwork(artwork_url):

    from PIL import Image
    import requests
    import os
    from io import BytesIO


    artwork_path = "data/current_artwork.jpg"
    temp_path = "data/current_artwork_tmp.jpg"

    # 1. Check that a URL was supplied
    if not artwork_url:
        print("[ARTWORK] No artwork URL provided.")
        return False

    print(f"[ARTWORK] Starting download: {artwork_url}")

    # 2. Ensure the data directory exists
    try:
        os.makedirs("data", exist_ok=True)

        # 3. Download artwork
        response = requests.get(artwork_url, timeout=15)
        response.raise_for_status()

        print(f"[ARTWORK] Download successful. Status: {response.status_code}")
        print(f"[ARTWORK] Downloaded {len(response.content)} bytes.")

        # 4. Load image into Pillow
        im = Image.open(BytesIO(response.content))
        im.load()

        print(f"[ARTWORK] Image loaded. Format: {im.format}, Size: {im.size}")

        # 5. Resize and convert to RGB
        out = im.convert("RGB").resize((400, 400))

        # 6. Save to temporary file
        out.save(temp_path, format="JPEG", quality=90)

        print("[ARTWORK] Temporary image saved.")

        # 7. Replace the existing image
        os.replace(temp_path, artwork_path)

        print(f"[ARTWORK] Artwork successfully saved to: {os.path.abspath(artwork_path)}")
        return True

    except requests.exceptions.RequestException as e:
        print(f"[ARTWORK ERROR] Download failed: {e}")

    except UnidentifiedImageError as e:
        print(f"[ARTWORK ERROR] The downloaded data is not a recognised image: {e}")

    except (OSError, ValueError) as e:
        print(f"[ARTWORK ERROR] Image processing or file operation failed: {e}")

    finally:
        # Remove any leftover temporary file
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except OSError as e:
                print(f"[ARTWORK WARNING] Could not remove temporary file: {e}")

    return False

if __name__ == "__main__":    
    result = update_artwork(artwork_url)
    print (f"final returned: {result}")