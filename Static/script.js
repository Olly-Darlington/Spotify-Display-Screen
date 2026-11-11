async function updateDisplay() {

    try {

        const response = await fetch('/api/now-playing');

        if (!response.ok) {
            throw new Error('Failed to retrieve track data');
        }

        const track = await response.json();

        if (!track.track_id) {
            return;
        }

        // Update track information
        document.getElementById('track-title').textContent = track.title;
        document.getElementById('track-artist').textContent = track.artist;
        document.getElementById('track-album').textContent = track.album;
        
        fitTrackInformation();


        const TrackArtwork = document.getElementById('track-artwork');

        if (!TrackArtwork) {
            throw new Error('Album artwork element not found');
        }

        // Only load a new image when the track changes
        if (TrackArtwork.dataset.trackId !== track.track_id) {

            TrackArtwork.src = `/api/vinyl?track_id=${encodeURIComponent(track.track_id)}`;

            TrackArtwork.dataset.trackId = track.track_id;
        }

        // Control vinyl rotation
        TrackArtwork.style.animationPlayState =
            track.is_playing ? "running" : "paused";

        // Update progress bar
        updateProgress(track.progress_ms, track.duration_ms);

    } catch (error) {

        console.error('Display update failed:', error);

    }
}

function fitTrackInformation() {

    const heading = document.getElementById('track-heading');
    const title = document.getElementById('track-title');
    const album = document.getElementById('track-album');

    if (!heading || !title || !album) {
        console.error('artist/album elements not found');
        return;
    }

    const maxFontSize = 18;
    const minFontSize = 11;

    // Reset to the normal layout before measuring
    heading.classList.remove('stacked');

    artist.style.fontSize = `${maxFontSize}px`;
    album.style.fontSize = `${maxFontSize}px`;

    // Try progressively smaller font sizes
    let fontSize = maxFontSize;

    while (heading.scrollWidth > heading.clientWidth &&
           fontSize > minFontSize) {

        fontSize -= 1;
        artist.style.fontSize = `${maxFontSize}px`;
        album.style.fontSize = `${maxFontSize}px`;
    }

    // If it still doesn't fit, stack the title and artist
    if (heading.scrollWidth > heading.clientWidth) {

        heading.classList.add('stacked');

        artist.style.fontSize = `${maxFontSize}px`;
        album.style.fontSize = `${maxFontSize}px`;
    }
}


function updateProgress(progress, duration) {

    if (progress == null || !duration || duration <= 0) {
        return;
    }

    const percentage = Math.min(
        100,
        Math.max(0, (progress / duration) * 100)
    );

    const progressBar = document.getElementById('progress-bar');

    if (!progressBar) {
        console.error('Progress bar element not found');
        return;
    }

    if (percentage === 0) {
        progressBar.style.transition = 'none';
    } else {
        progressBar.style.transition = 'width 3s linear';
    }

    progressBar.style.width = `${percentage}%`;
}


updateDisplay();

setInterval(updateDisplay, 3000);
