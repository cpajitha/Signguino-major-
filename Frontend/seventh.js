let videoStream;
let capturing = false;

async function startCamera() {
    try {
        const constraints = { video: true };
        if (!capturing) {
            videoStream = await navigator.mediaDevices.getUserMedia(constraints);
            const videoElement = document.getElementById('videoElement');
            videoElement.srcObject = videoStream;
            capturing = true;
        } else {
            stopCamera();
        }
    } catch (error) {
        console.error('Error accessing camera:', error);
        alert('Failed to access camera. Please ensure it is enabled and try again.');
    }
}

function stopCamera() {
    if (videoStream) {
        videoStream.getTracks().forEach(track => track.stop());
        capturing = false;
    }
}

async function translateSign() {
    try {
        if (!capturing) {
            alert('Please start the camera before translating.');
            return;
        }

        const videoElement = document.getElementById('videoElement');
        const canvas = document.createElement('canvas');
        canvas.width = videoElement.videoWidth;
        canvas.height = videoElement.videoHeight;
        canvas.getContext('2d').drawImage(videoElement, 0, 0, canvas.width, canvas.height);
        const imageDataURL = canvas.toDataURL('image/jpeg');

        // Send the captured image to the backend for recognition
        const formData = new FormData();
        formData.append('files', dataURLtoBlob(imageDataURL), 'image.jpg');

        const response = await fetch('http://localhost:8000/translate', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Failed to translate sign language. HTTP status code: ' + response.status);
        }

        const data = await response.json();
        const wordTextArea = document.getElementById('wordTextArea');
        wordTextArea.value = data.recognized_word;

        // Speak the recognized word
        speakWord(data.recognized_word);
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while translating sign language. Please try again.');
    }
}

function speakWord(word) {
    const speech = new SpeechSynthesisUtterance(word);
    speech.lang = 'en-US';
    window.speechSynthesis.speak(speech);
}


// Convert data URL to blob function remains the same

function dataURLtoBlob(dataURL) {
    try {
        const arr = dataURL.split(',');
        const mime = arr[0].match(/:(.*?);/)[1];
        const bstr = atob(arr[1]);
        let n = bstr.length;
        const u8arr = new Uint8Array(n);
        while (n--) {
            u8arr[n] = bstr.charCodeAt(n);
        }
        return new Blob([u8arr], { type: mime });
    } catch (error) {
        console.error('Error converting data URL to blob:', error);
        return null; // Return null if an error occurs
    }
}
// Call startCamera function when the page is loaded
startCamera();
