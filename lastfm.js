function updateNowPlaying() {
  fetch('https://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=jazzifyy&api_key=c40f88ab4a1cffd62776865a8e684a8e&format=json')
    .then(response => response.json())
    .then(data => {
      const container = document.getElementById('lastfm-widget');

      if (data.recenttracks && data.recenttracks.track.length > 0) {
        const track = data.recenttracks.track[0];
        const imageUrl = track.image?.[3]?.['#text'] || '';
	  
// The specific hash Last.fm uses for the "star" placeholder
const placeholderHash = '2a96cbd8b46e442fc41c2b86b821562f';

// Check if image is truly empty OR if it contains the placeholder hash
const hasRealArt = imageUrl !== '' && !imageUrl.includes(placeholderHash);

// Only create the img tag if we have real art
const albumArt = hasRealArt 
  ? `<img src="${imageUrl}" class="lastfm-img">` 
  : '';

// Add a 'no-art' class to the container if we are hiding the image
const containerClass = hasRealArt ? 'lastfm-track' : 'lastfm-track no-art';
        const trackHtml = `
          <div class="lastfm-track">
            ${albumArt}
            <div class="track-text">
              <p><strong>${track.name}</strong></p>
              <p>by ${track.artist['#text']}</p>
            </div>
          </div>
        `;

        container.innerHTML = trackHtml;
      } else {
        container.innerHTML = '<p>No recent tracks found.</p>';
      }
    })
    .catch(error => {
      console.error('Error fetching Last.fm data:', error);
      document.getElementById('lastfm-widget').innerHTML = '<p>Error loading track info.</p>';
    });
}

// Run once and every 10 seconds
updateNowPlaying();
setInterval(updateNowPlaying, 10000);

