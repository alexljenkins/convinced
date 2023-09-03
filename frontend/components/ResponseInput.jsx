"use client";
import { useState } from 'react';
import { Button, Loading } from "@nextui-org/react";
// https://nextui.org/docs/components/button

import { submitEarthlingsMessage } from "@components/api/InputSubmit";

const ResponseInput = ({ handleAIResponse }) => {
  const [busy, setBusy] = useState(false);
  const [response, setResponse] = useState("");
  const [error, setError] = useState("");

  const handleInputChange = (e) => {
    setResponse(e.target.value);
  };

  const handleFormSubmit = async (e) => {
    if (busy) {
      return; // Exit early if click is already in progress
    }
    setBusy(true);
    e.preventDefault();
    e.stopPropagation();
    setError("");
    console.log(response);
    const wordCount = response.trim().split(/\s+/).length;

    if (wordCount <= 10) {
      setError("Your message can't be that convincing if it's that short. Remember, this is to save all of humanity!");
      setBusy(false);
      return;
    }
    if (wordCount > 200) {
      setError(`Your message seems to drag on a bit, we fear the aliens will get bored and stop reading. Shorten it to less than 200 words. It's currently ${wordCount} words.`);
      setBusy(false);
      return;
    }

    const timeoutPromise = new Promise((resolve) => setTimeout(() => resolve('Timeout occurred'), 100000));
    const backendPromise = submitEarthlingsMessage(response);
    try {
      const result = await Promise.race([timeoutPromise, backendPromise]);
      // Handle the result from the backend or the timeout
      if (result === 'Timeout occurred') {
        setError("Message took too long to get to the aliens. Please try again later.")
        setBusy(false);
      } else {
        // Handle successful backend response
        handleAIResponse(result);
      }
      } catch (error) {
      // Handle any other errors
      console.error('An error occurred while sending the request to backend:', error);
      setError("Something went wrong with the message. Please try again later.")
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
          minLength="10" // Set minimum character length to 10
          maxLength="1500" // Set maximum character length to 800
          disabled={busy}
        />
        {error && <p className="text-red-500">{error}</p>} {/* Display the error message */}
        <div className='pt-3 mx-3 mb-5 gap-4 flex-end'>
          <Button bordered color="warning" //auto // error
            type='submit'
            disabled={busy}
            className='w-full md:w-auto text-lg px-8 py-1.5 rounded-lg md:text-sm md:px-5'
          >
            
            {busy ? <Loading color="currentColor" size="sm" /> : 'Send Message'}
          </Button>
        </div>
      </form>
    );
  };

export default ResponseInput;
