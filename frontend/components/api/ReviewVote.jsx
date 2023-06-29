import { fetchApiKey } from '@components/keys';

export const sendVote = async (winnerId, other_id, ifWinsValue) => {
    console.log('Sending data: ', winnerId, other_id, ifWinsValue);
    const apiKey = fetchApiKey();
    try {
      const response = await fetch('http://localhost:8000/api/vote', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': apiKey,
        },
          body: JSON.stringify({
            "winner_id": winnerId,
            "loser_id": other_id,
            "points_change": ifWinsValue
          }),
        });
      if (response.ok) {
        // Vote sent successfully
        console.log('Vote sent!');
      } else {
        // Handle error case
        console.error('Failed to send vote.');
      }
    } catch (error) {
      console.error('Failed to send vote:', error);
    }
  };