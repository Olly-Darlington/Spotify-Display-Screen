from flask import Flask, jsonify, send_file, render_template 
from threading import Lock
import os

# Initialise Flask
app = Flask(__name__)


# Shared playback information
playback_state = None
state_lock = Lock()


def set_now_playing(track_info):
    global playback_state

    with state_lock:
        playback_state = track_info.copy() if track_info else None

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "online",
        "message": "Spotify display server running"
     }), 200


# Song Details
@app.route('/api/now-playing', methods=['GET'])
def now_playing():

    with state_lock:
        track_data = playback_state.copy() if playback_state else None

    if track_data is None:
            return jsonify({"message": "Nothing currently playing"}), 200

    return jsonify(track_data)

# Artwork
@app.route('/api/artwork', methods=['GET'])
def get_artwork():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    artwork_path = os.path.join(
        base_dir, "data", "current_artwork.jpg"
    )

    if not os.path.exists(artwork_path):
        return jsonify({
            "error": "Artwork file not found"
        }), 404

    return send_file(
        artwork_path,
        mimetype='image/jpeg'
    )


# Vinyl image
@app.route('/api/vinyl', methods=['GET'])
def get_vinyl_artwork():

    base_dir = os.path.dirname(os.path.abspath(__file__))
    vinyl_path = os.path.join(
        base_dir, "data", "current_vinyl.png"
    )

    if not os.path.exists(vinyl_path):
        return jsonify({
            "error": "Vinyl artwork file not found"
        }), 404

    response = send_file(
        vinyl_path,
        mimetype='image/png'
    )

    response.headers["Cache-Control"] = "no-store"

    return response


# Display output
@app.route('/')
def home():
    return render_template('index.html')


# Run the server
if __name__ == "__main__":
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True
    )   
