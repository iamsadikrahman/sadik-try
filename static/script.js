// // script.js
// const generateButton = document.getElementById('generate');
// const promptInput = document.getElementById('prompt');
// const outputDiv = document.getElementById('output');

// generateButton.addEventListener('click', () => {
//     const prompt = promptInput.value;

//     fetch('/generate', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/x-www-form-urlencoded',
//         },
//         body: `prompt=${prompt}`,
//     })
//     .then(response => {
//         console.log('Response received:', response);
//         response.text()
//     })
//     .then(generatedContent => {
//         outputDiv.textContent = generatedContent;
//     })
//     .catch(error => {
//         console.error('Error:', error);
//         outputDiv.textContent = 'কন্টেন্ট তৈরি করতে সমস্যা হয়েছে। অনুগ্রহ করে পরে আবার চেষ্টা করুন।';
//     });
// });


const generateButton = document.getElementById('generate');
const promptInput = document.getElementById('prompt');
const outputDiv = document.getElementById('output');

generateButton.addEventListener('click', () => {
    const prompt = promptInput.value;

    fetch('/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `prompt=${prompt}`,
    })
    .then(response => {
        console.log('Response received:', response); 
        return response.text();
    })
    .then(generatedContent => {
        console.log('Generated content:', generatedContent);
        outputDiv.innerHTML = generatedContent; 
    })
    .catch(error => {
        console.error('Error:', error);
        outputDiv.textContent = 'কন্টেন্ট তৈরি করতে সমস্যা হয়েছে। অনুগ্রহ করে পরে আবার চেষ্টা করুন।';
    });
});