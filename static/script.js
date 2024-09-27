const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const captureButton = document.getElementById('capture');
const resultImage = document.getElementById('resultImage');
const backgroundVideo = document.getElementById('backgroundVideo');
const body = document.body;

// Access the user's webcam
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
    })
    .catch(err => {
        console.error("Error accessing the camera: ", err);
    });

// Capture the image from the video stream and send to Flask
captureButton.addEventListener('click', async () => {
    const context = canvas.getContext('2d');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Convert the canvas to an image
    const imageDataURL = canvas.toDataURL('image/png');

    // Send the image data to the Flask server
    const response = await fetch('/upload', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ image: imageDataURL })
    });

    const result = await response.json();
    console.log(result);

    if (!result.prediction) {
        console.log(result.alert)
        alert(result.alert);  // Now the alert will show correctly
    }

    // Check the prediction result from the server response
    if (result.prediction === 1) {  // 1 corresponds to "Helmet" class
        // Change the background to the video
        backgroundVideo.classList.remove('hidden');
        body.style.backgroundImage = 'none';  // Remove the background image
    } else {
        // Revert to the background image
        backgroundVideo.classList.add('hidden');
        body.style.backgroundImage = 'url("/static/road_photo.png")';  // Set the background image
    }
});
