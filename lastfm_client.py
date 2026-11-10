import os
import requests


LASTFM_API_KEY = os.getenv("LASTFM_API_KEY")
LASTFM_URL = "https://ws.audioscrobbler.com/2.0/"

def get_track_genres(artist, title):
    if not LASTFM_API_KEY:
        print("[LASTFM ERROR] API key is missing.")
        return []

    params = {
        "method": "track.getTopTags",
        "artist": artist,
        "track": title,
        "api_key": LASTFM_API_KEY,
        "autocorrect": 1,
        "format": "json"
    }

    try:
        response = requests.get(
            LASTFM_URL,
            params=params,
            timeout=10
        )

        response.raise_for_status()
        data = response.json()

        # error handeling
        if "error" in data:
            print(f"[LASTFM ERROR] {data['message']}")
            return []

        tags = data.get("toptags", {}).get("tag", [])

        if isinstance(tags, dict):
            tags = [tags]

        return[
            tag['name']
            for tag in tags
        ]

    except (requests.RequestException, ValueError) as e:
        print(f"[LASTFM ERROR] request failed: {e}")
        return
