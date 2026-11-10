import time
import threading

from spotify_client import initialise_spotipy, get_current_track_info
from image_handelling import update_artwork
from app import app, set_now_playing
from listening_log import log_track


# How often to check Spotify, in seconds
POLL_INTERVAL = 3

def run_server():
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
        use_reloader=False
    )


def main():

    print("[MAIN] Starting Spotify display.")

    # Initialise Spotipy
    sp = initialise_spotipy()

    if sp is None:
        print("[MAIN] Could not initialise Spotify. Shutting down.")
        return


    # Start Flask in a separate background thread
    server_thread = threading.Thread(
        target=run_server,
        daemon=True
    )

    server_thread.start()

    print("[MAIN] Flask server started.")

    # Remember the last track processed
    last_track_id = None

    # Spotify polling loop
    while True:

        try:
            print("[MAIN] Checking Spotify...")

            # Get current track information
            track_info = get_current_track_info(sp)

            # Check whether Spotify returned a track
            if not track_info:
                print("[MAIN] No track currently playing.")
                set_now_playing(None)

                time.sleep(POLL_INTERVAL)
                continue

            # Extract track ID
            track_id = track_info.get("track_id")

            if not track_id:
                print("[MAIN] Track information has no track ID.")
                time.sleep(POLL_INTERVAL)
                continue

            # Check whether the track has changed
            if track_id != last_track_id:

                print("[MAIN] New track detected.")

                artwork_url = track_info.get("artwork_url")

                log_track(track_info)

                # Update album artwork
                artwork_success = update_artwork(artwork_url)

                if not artwork_success:
                    print("[MAIN] Artwork update failed. Will retry.")
                    time.sleep(POLL_INTERVAL)
                    continue

                # Only mark the track as processed after artwork succeeds
                last_track_id = track_id

            # 6. Update Flask with the latest Spotify information
            set_now_playing(track_info)

            print(
                f"[MAIN] Now playing: "
                f"{track_info.get('title')} - "
                f"{track_info.get('artist')}"
            )

        except Exception as e:
            print(f"[MAIN ERROR] {e}")

        # 7. Wait before checking Spotify again
        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print("\n[MAIN] Spotify display shutting down.")
