import { fetchApiKey } from '@components/keys';

export const fetchReviewData = async () => {
    const apiKey = fetchApiKey();
    try {
      const apiResponse = await fetch('http://localhost:8000/api/collect_responses', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': apiKey,
        },
        body: JSON.stringify({}),
      });
    if (apiResponse.ok) {
      const data = await apiResponse.json();
      console.log('Request recieved:', data);
      return data;
    } else {
      // Handle the error response
      console.error('Request failed with status:', apiResponse);
      return {'response': [{ 'user_input': 'Earth is sleeping' }, { 'user_input': 'Earth is sleeping' }]};
    }
  } catch (error) {
  console.error('An error occurred:', error);
  return {'response': [{ 'user_input': 'Earth is sleeping...' }, { 'user_input': 'Earth is sleeping...' }]};
  }
};