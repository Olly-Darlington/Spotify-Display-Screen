import os
import requests
from dotenv import load_dotenv

load_dotenv()

LASTFM_API_KEY = os.environ.get("LASTFM_API_KEY")
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

        # print("[DEBUG] Last.fm status:", response.status_code)
        # print("[DEBUG] Last.fm response:", data)
        
        # error handeling
        if "error" in data:
            print(f"[LASTFM ERROR] {data['message']}")
            return []

        tags = data.get("toptags", {}).get("tag", [])

        # print("[DEBUG] Extracted tags:", tags)

        if isinstance(tags, dict):
            tags = [tags]

        genres = [
            tag["name"]
            for tag in tags
            if tag.get("name")
        ]

        # Fall back to artist-level tags
        if not genres:
            print("[LASTFM] No track tags found. Trying artist tags.")

            params["method"] = "artist.getTopTags"
            params.pop("track")

            response = requests.get(
                LASTFM_URL,
                params=params,
                timeout=10
            )

            response.raise_for_status()
            data = response.json()

            tags = data.get("toptags", {}).get("tag", [])

            if isinstance(tags, dict):
                tags = [tags]

            genres = [
                tag["name"]
                for tag in tags
                if tag.get("name")
            ]

        return genres

    except (requests.RequestException, ValueError) as e:
        print(f"[LASTFM ERROR] Request failed: {e}")
        return []
