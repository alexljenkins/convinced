import { useState } from 'react';

const ResponseInput = ({ submitting, handleSubmit }) => {
  const [response, setResponse] = useState("");
  const [key, setKey] = useState("alexisthebestchuckouttherest"); // should probably not have key here

  const handleInputChange = (e) => {
    setResponse(e.target.value);
  };

  const handleFormSubmit = async (e) => {
    e.preventDefault();
    console.log(response);
    try {
      const apiResponse = await fetch('http://localhost:8000/api/ask_character_ai', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ response, key }),
      });

      if (apiResponse.ok) {
        const data = await apiResponse.json();
        console.log('Response received from backend:', data.response);
        handleSubmit(data.response); // Handle the response here
      } else {
        console.error('Failed to send request to backend');
      }
    } catch (error) {
      console.error('An error occurred while sending the request to backend:', error);
    }
  };

  return (
    <form onSubmit={handleFormSubmit} className='w-full max-w-2xl flex flex-col'>
      <textarea
        value={response}
        onChange={handleInputChange}
        placeholder='Write your message to the aliens...'
        required
        className='response_input_text_area'
      />
      <div className='pt-3 mx-3 mb-5 gap-4 flex-end'>
        <button
          type='submit'
          disabled={submitting}
          className='w-full md:w-auto text-lg px-8 py-1.5 bg-primary-orange rounded-lg text-white md:text-sm md:px-5'
        >
          {submitting ? `Sending...` : 'Submit'}
        </button>
      </div>
    </form>
  );
};

export default ResponseInput;
