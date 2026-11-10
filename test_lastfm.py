from lastfm_client import get_track_genres


genres = get_track_genres(
    "The Beatles",
    "While My Guitar Gently Weeps - Remastered 2009"
)

print("Returned tags:", genres)