import { useState } from 'react';
import { Button, Loading } from "@nextui-org/react";
// https://nextui.org/docs/components/button

import { submitEarthlingsMessage } from "@components/api/InputSubmit";
{/* <Button disabled auto bordered color="primary" css={{ px: "$13" }}>
  <Loading color="currentColor" size="sm" />
</Button> */}


const ResponseInput = ({ handleAIResponse }) => {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [response, setResponse] = useState("");
  const [error, setError] = useState("");

  const handleInputChange = (e) => {
    setResponse(e.target.value);
  };

  const handleFormSubmit = async (e) => {
    setIsSubmitting(true);
    e.preventDefault();
    setError("");
    // await new Promise((r) => setTimeout(r, 10000)); // wait 10 seconds for testing
    console.log(response);
    const wordCount = response.trim().split(/\s+/).length;

    if (wordCount < 10 || wordCount > 200) {
      setError("Response length should be between 10 and 200 words.");
      setIsSubmitting(false);
      return;
    }
    handleAIResponse(submitEarthlingsMessage(response));
    setIsSubmitting(false);
    };

    return (
      <form onSubmit={handleFormSubmit} className='w-full max-w-2xl flex flex-col'>
        <textarea
          value={response}
          onChange={handleInputChange}
          placeholder='Write your message to the aliens...'
          required
          className='response_input_text_area'
          // minLength="20" // Set minimum character length to 10
          // maxLength="800" // Set maximum character length to 800
          disabled={isSubmitting}
        />
        {error && <p className="text-red-500">{error}</p>} {/* Display the error message */}
        <div className='pt-3 mx-3 mb-5 gap-4 flex-end'>
          <Button bordered color="error" auto
            type='submit'
            disabled={isSubmitting}
            className='w-full md:w-auto text-lg px-8 py-1.5 bg-primary-orange rounded-lg text-white md:text-sm md:px-5'
          >
            {isSubmitting ? `Sending...` : 'Send Message'}
          </Button>
        </div>
      </form>
    );
  };

export default ResponseInput;
