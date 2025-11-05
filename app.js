document.addEventListener('DOMContentLoaded', () => {

    const btnGetStatus = document.getElementById('btn-get-status');
    const btnPostData = document.getElementById('btn-post-data');
    const responseOutput = document.getElementById('response-output');

    const API_BASE_URL = 'http://localhost:8000';

    function showResponse(text, isError = false) {
        responseOutput.textContent = text;
        responseOutput.style.color = isError ? '#ff6b6b' : '#f0f0f0';
    }
    async function handleGetStatus() {
        showResponse('Надсилаю запит GET /status...');
        try {
            const response = await fetch(`${API_BASE_URL}/status`);
            
            if (!response.ok) {
                throw new Error(`Помилка HTTP: ${response.status} ${response.statusText}`);
            }
            
            const data = await response.json();
            showResponse(JSON.stringify(data, null, 2));

        } catch (error) {
            console.error('Помилка в handleGetStatus:', error);
            showResponse(`Помилка: ${error.message}`, true);
        }
    }

    async function handlePostData() {
        showResponse('Надсилаю запит POST /data...');
        
        const postData = {
            name: "Alice",
            age: 25
        };

        try {
            const response = await fetch(`${API_BASE_URL}/data`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(postData) 
            });

            const responseData = await response.json();

            if (!response.ok) {
                const errorText = responseData.error || `Помилка HTTP: ${response.status}`;
                throw new Error(errorText);
            }

            showResponse(JSON.stringify(responseData, null, 2));

        } catch (error) {
            console.error('Помилка в handlePostData:', error);
            showResponse(`Помилка: ${error.message}`, true);
        }
    }
    btnGetStatus.addEventListener('click', handleGetStatus);
    btnPostData.addEventListener('click', handlePostData);
});