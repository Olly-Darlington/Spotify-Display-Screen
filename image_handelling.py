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


from PIL import Image, UnidentifiedImageError, ImageDraw, ImageOps
import requests
import os
from io import BytesIO

def update_artwork(artwork_url):


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

        # print(f"[ARTWORK] Download successful. Status: {response.status_code}")
        # print(f"[ARTWORK] Downloaded {len(response.content)} bytes.")

        # 4. Load image into Pillow
        im = Image.open(BytesIO(response.content))

        # print(f"[ARTWORK] Image loaded. Format: {im.format}, Size: {im.size}")

        # 5. Resize and convert to RGB
        out = im.convert("RGB").resize((400, 400))

        # 6. Save to temporary file
        out.save(temp_path, format="JPEG", quality=90)

        # print("[ARTWORK] Temporary image saved.")

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



def create_vinyl_artwork():
    # Convert current album art into a mock spinning record

    base_dir = os.path.dirname(os.path.abspath(__file__))


    artwork_path = os.path.join(
        base_dir, "data", "current_artwork.jpg"
    )

    vinyl_path = os.path.join(
        base_dir, "data", "current_vinyl.png"
    )

    # Process image at double resolution to have smoother post-compression result
    size = 800
    centre = size // 2
    disc_radius = 396

    try:
        # Creating canvas
        vinyl = Image.new(
            "RGBA", (size, size), (0,0,0,0)
        )

        draw = ImageDraw.Draw(vinyl)


        # Drawing black vinyl disc
        draw.ellipse(
            (
                centre - disc_radius,
                centre - disc_radius,
                centre + disc_radius,
                centre + disc_radius
            ),
            fill=(22, 22, 24, 225)
        )

        # add subtle concentric grooves
        for radius in range(145, 385, 8):

            draw.ellipse(
                (
                    centre - radius,
                    centre - radius,
                    centre + radius,
                    centre + radius                    
                ),
                outline=(65, 65, 70, 180), width=2
            )

            draw.ellipse(
                (
                    centre - radius + 3,
                    centre - radius + 3,
                    centre + radius - 3,                   
                    centre + radius - 3,
                ),
                outline=(8, 8, 10, 180), width=2
            )

        # Add album art to centre
        label_size = 300

        with Image.open(artwork_path) as artwork:
            artwork = ImageOps.fit(
                artwork.convert("RGB"),
                (label_size, label_size),
                method=Image.Resampling.LANCZOS
            )

        # Creates circular mask for artwork
        mask = Image.new("L", (label_size, label_size), 0)
        mask_draw = ImageDraw.Draw(mask)

        mask_draw.ellipse(
            (0, 0, label_size - 1, label_size - 1),
            fill=255
        )

        # Place album art in centre of the image
        vinyl.paste(
            artwork, (
                centre - label_size // 2,
                centre - label_size // 2
                ),
            mask 
        )

        draw = ImageDraw.Draw(vinyl)

        # Add subtle boarder around the artwork 'sticker'
        draw.ellipse(
            (
                centre - 156,
                centre - 156,  
                centre + 156,
                centre + 156                                              
            ), 
            outline=(130, 130, 135, 200),
            width=3
        )


        # Create hole in centre of record
        hole_radius = 9

        draw.ellipse(
            (
                centre - hole_radius,
                centre - hole_radius,
                centre + hole_radius,
                centre + hole_radius                
            ), fill=(0, 0, 0, 0)
        )


        # Downsize to fit display
        vinyl = vinyl.resize(
            (400, 400), Image.Resampling.LANCZOS
        )


        # Save vinyl render as PNG
        vinyl.save(vinyl_path, format='PNG')

        print("[ARTWORK] Image sucessfully converted to vinyl art.")

        return True
    except Exception as e:
        print(f"[ARTWORK] ERROR - Vinyl genreation failed: {e}")
        return False



if __name__ == "__main__":    
    result = update_artwork(artwork_url)
    print (f"final returned: {result}")