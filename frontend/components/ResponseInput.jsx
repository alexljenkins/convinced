import { useState } from 'react';

const ResponseInput = ({ submitting, handleSubmit }) => {
  const [response, setResponse] = useState("");

  const handleInputChange = (e) => {
    setResponse(e.target.value);
  };

  const handleFormSubmit = async (e) => {
    e.preventDefault();

    try {
      const apiResponse = await fetch('/api/submit-response', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ response }),
      });

      if (apiResponse.ok) {
        console.log('Text sent to Python backend successfully!');
        handleSubmit(response); // Handle the submit action here
      } else {
        console.error('Failed to send text to Python backend');
      }
    } catch (error) {
      console.error('An error occurred while sending text to Python backend', error);
    }
  };

  return (
    <form
      onSubmit={handleFormSubmit}
      className='w-full max-w-2xl flex flex-col'
    >
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
