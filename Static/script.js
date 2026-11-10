async function updateDisplay() {

    try {

        const response = await fetch('/api/now-playing');

        if (!response.ok) {
            throw new Error(`failed to retrieve track data`);
        }

        const track = await response.json();

        if (!track.track_id) {
            return;
        }

        // Update the track info on the page
        document.getElementById('track-title').textContent = track.title;
        document.getElementById('track-artist').textContent = track.artist;
        document.getElementById('track-album').textContent = track.album;
        
        document.getElementById('track-artwork').src = 
            `/api/artwork?track_id=${encodeURIComponent(track.track_id)}`;  
        
        updateProgress(track.progress_ms, track.duration_ms);

} catch (error) {

        console.error('Display update failed:', error);

    }
}

// FIX progress bar - changed scaleX scaleFactor to try and smooth animation but it broke
function updateProgress(progress, duration) {

    if (!duration || duration <= 0) {
        return;
    }



    const percentage = (progress / duration) * 100;
    const progressBar = document.getElementById('progress-bar');

    // If it's a reset (0%), snap to it instantly. Otherwise, animate over 3s.
    if (percentage === 0) {
        progressBar.style.transition = 'none';
    } else {
        progressBar.style.transition = 'width 3s linear';
    }

    progressBar.style.width = `${percentage}%`;
}


updateDisplay();

setInterval(updateDisplay, 3000);
