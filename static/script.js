//permision
navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } }) //back camera
    .then(function(stream) {
        var video = document.getElementById('video');
        video.srcObject = stream;
        video.play();
    })
    .catch(function(err) {
        console.log("An error occurred: " + err);
    });

// Function to reload the index.html content
function reloadPageContent() {
    // Make a GET request to the server to fetch updated HTML content
    fetch('/index.html')
        .then(response => response.text())
        .then(html => {
            // Update the HTML content of the page
            document.body.innerHTML = html;
        })
        .catch(error => {
            console.error('Error fetching page content:', error);
        });
}

// Capture photo from the video stream
document.getElementById('takePhotoBtn').addEventListener('click', function() {
    var video = document.getElementById('video');
    var canvas = document.getElementById('canvas');
    var context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    var dataURL = canvas.toDataURL('image/png');

    fetch('/upload', {
        method: 'POST',
        body: dataURL
    }).then(response => {
        if (response.ok) {
            console.log('Image uploaded successfully');
            reloadPageContent();
        } else {
            console.error('Error uploading image');
        }
    }).catch(error => {
        console.error('Error uploading image:', error);
    });
});
