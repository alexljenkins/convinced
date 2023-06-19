"use client"
import { useState } from 'react';
import ResponseInput from "@components/ResponseInput";
import EarthCanvas from "@components/canvas/Earth";


const Home = () => {
  const [submitting, setSubmitting] = useState(false);
  const [response, setResponse] = useState(null);

  const handleSubmit = (response) => {
    // Handle the response submission logic here
    console.log("Submitted response:", response);
    setSubmitting(true);

    setResponse(response);
    // Simulating asynchronous submission
    setTimeout(() => {
      setSubmitting(false);
    }, 20000);
  };

  return (
    <div className='w-full flex-center flex-col 2xl:mt-10 stacked_containers'>
      <h1 className='head_text orange_gradient text-center top_content'>
        Can You Save Earth?
      </h1>
      <p className='flex-center flex-col py-0 mt-2 sm:mt-0 xl:mt-5 bottom_spacing'></p>
      {response ? (
        <div className='flex-center flex-col mt-8 lg:mt-10 xl:mt-16 2xl:mb-20 bottom_spacing'></div>
        ) : (
          <p className='desc text-center flex-col top_content'>
            An advanced alien ship is on its way to Earth...<br />
            Can you convince them not to destroy us?
          </p>
      )}
      <div className='flex-center flex-col mt-20 xl:mt-20 2xl:mb-24 bottom_spacing'></div>
      
      {response ? (
        <div className='flex-center flex-col top_content'>
          <p className='ai_response_area ai_response text-center flex-col top_content'>{response}</p>
        </div>
        ) : (
          <div className='w-full flex-center flex-col top_content'>
            <ResponseInput submitting={submitting} handleSubmit={handleSubmit} />
          </div>
        )}
      
      <div className='w-full flex-center flex-col mt-14 xl:mt-4 2xl:mt-20 h-[500px] sm:h-[700px] xl:h-[800px] 2xl:h-[900px] behind_div'>
        <EarthCanvas />
      </div>
  </div>
  );
};

export default Home;


