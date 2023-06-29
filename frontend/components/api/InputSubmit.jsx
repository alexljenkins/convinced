import { fetchApiKey } from '@components/keys';

export const submitEarthlingsMessage = async (user_input) => {
    const apiKey = fetchApiKey();
    try {
        const apiResponse = await fetch('http://localhost:8000/api/ask_character_ai', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': apiKey,
            },
            body: JSON.stringify({ user_input }),
        });

        if (apiResponse.ok) {
            const data = await apiResponse.json();
            console.log('Response received from backend:', data.response);
            return data.response
        } else {
            console.error('Failed to send request to backend');
            return 'Failed to send request to backend';
        }
    } catch (error) {
        console.error('An error occurred while sending the request to backend:', error);
        return 'Failed to send request to backend';
    }
};
