import os
import pandas as pd
from datetime import datetime, timezone


Base_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_path = os.path.join(Base_DIR, "data", "listening_history.csv")

def log_track(track_info):

    if not track_info:
        return

    record = {
        "track_id": track_info.get("track_id"),
        "title": track_info.get("title"),
        "artist": track_info.get("artist"),
        "album": track_info.get("album"),
        "genres": "; ".join(track_info.get("genres", [])),       
        "duration_ms": track_info.get("duration_ms"),
        "started_at": datetime.now(timezone.utc).isoformat()
    }

    # print("[DEBUG] Genres being written:", record["genres"])

    df = pd.DataFrame([record])

    os.makedirs(os.path.dirname(CSV_path), exist_ok=True)

    df.to_csv(
        CSV_path,
        mode='a',
        header=not os.path.exists(CSV_path),
        index = False
    )

    print(f"[LOGGER] Recorded: {record['title']} - {record['artist']}")