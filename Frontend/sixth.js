async function translateSign() {
    const fileInput = document.getElementById('fileInput');
    const files = fileInput.files;

    if (files.length === 0) {
        alert('Please select at least one image.');
        return;
    }

    try {
        const formData = new FormData();
        const recognizedWords = []; // Array to store recognized words
        for (let i = 0; i < files.length; i++) {
            formData.append('files', files[i]);
            displayImage(files[i]); // Display each selected image

            // Fetch recognition result for each image
            const response = await fetch('http://localhost:8000/translate', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Failed to translate sign language. HTTP status code: ' + response.status);
            }

            const data = await response.json();
            recognizedWords.push(data.recognized_word);


            formData.delete('files'); // Clear FormData for the next iteration
            
            // Append recognized word to the textarea
            const wordTextArea = document.getElementById('wordTextArea');
            wordTextArea.value += data.recognized_word + '';
        }
        speakWord(wordTextArea.value);

        // Enable the audio button
        document.getElementById('audioButton').disabled = false; 
    } catch (error) {
        console.error('Error:', error);
        //alert('An error occurred while translating sign language. Please try again.');
    }
}

function speakWord(word) {
    const speech = new SpeechSynthesisUtterance(word);
    speech.lang = 'en-US';
    window.speechSynthesis.speak(speech);
}

function displayImage(file) {
    const uploadedImagesContainer = document.getElementById('uploadedImages');
    const image = document.createElement('img');
    image.src = URL.createObjectURL(file);
    image.width = 200; // Set image width as needed
    uploadedImagesContainer.appendChild(image);
}


function base64toBlob(base64Data) {
    const byteCharacters = atob(base64Data);
    const byteNumbers = new Array(byteCharacters.length);
    for (let i = 0; i < byteCharacters.length; i++) {
        byteNumbers[i] = byteCharacters.charCodeAt(i);
    }
    const byteArray = new Uint8Array(byteNumbers);
    return new Blob([byteArray]);
}
