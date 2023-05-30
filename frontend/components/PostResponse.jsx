const postResponse = async (response_input) => {
    try {
      const response = await fetch('http://localhost:8000/api/endpoint', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ data: response_input }),
      });

      if (response.ok) {
        const data = await response.json();
        // Handle the response data
        console.log(data);
      } else {
        // Handle the error response
        console.error('Request failed with status:', response.status);
      }
    } catch (error) {
      console.error('An error occurred:', error);
    }
  };
  
postResponse();
