navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } }) // back camera
    .then(function(stream) {
        var video = document.getElementById('video');
        video.srcObject = stream;
        video.play();
    })
    .catch(function(err) {
        console.log("An error occurred: " + err);
    });

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
    }).then(response => response.text())
    .then(data => {
        if (data) {
            console.log(data);
            
            // Display the received text on the screen
            var textContainer = document.getElementById('textContainer');
            textContainer.innerText = data;

            // Optionally, fetch and display the processed image if available
            fetch('/image', {
                method: 'GET'
            })
            .then(response => response.blob())
            .then(blob => {
                var image = new Image();
                image.onload = function() {
                    // Draw the image onto the canvas
                    context.drawImage(image, 0, 0, canvas.width, canvas.height);
                };
                image.src = URL.createObjectURL(blob);
            })
            .catch(error => {
                console.error('Error fetching server response:', error);
            });
        } else {
            console.error('Error uploading image');
        }
    }).catch(error => {
        console.error('Error uploading image:', error);
    });
});
