"use client"
import VotingCard from "@components/VotingCard";

import { useState, useEffect } from 'react';

const Example = () => {
  const [cardcontent, setCardContent] = useState({ 'response': [{ 'user_input': 'Loading Data' },{'user_input': 'Please Wait...'}]});
  
  const fetchData = async () => {
    const apiResponse = await fetch('http://localhost:8000/api/collect_responses', {
      method: 'POST',
      headers: {'Content-Type': 'application/json',},
      body: JSON.stringify({ "key": "alexisthebestchuckouttherest" }),
    });

    const data = await apiResponse.json();
    setCardContent(data);
  };
  useEffect(() => {
    if (cardcontent.response[0].user_input === 'Loading Data') {
      fetchData();
    }
  }, []);
  const renderContent = () => {
    return (
      <div className='w-full flex-center flex-col 2xl:mt-10 stacked_containers'>
        <h1 className='head_text orange_gradient text-center top_content'>
          Would you let Earth live?
        </h1>
        <p className='flex-center flex-col py-0 mt-2 sm:mt-0 xl:mt-5 bottom_spacing'></p>
        <p className='desc text-center flex-col top_content'>
          If you were the alien, which of these messages<br />
          would convince you more to let Earth live?
          {/* {JSON.stringify(cardcontent['response'])} */}
          <button className='text-white black_btn' onClick={() => fetchData()}>Get Data</button>
        </p>
        <div className="container mx-auto px-4">
          <div className="grid gap-4 lg:grid-cols-2 text-white">
            <div>
              <VotingCard content={JSON.stringify(cardcontent['response'][0]['user_input'])} fetcher = {fetchData} />
            </div>
            <div>
              <VotingCard content={JSON.stringify(cardcontent['response'][1]['user_input'])} fetcher = {fetchData} />
            </div>
          </div>
        </div>
        <div className='w-full flex-center flex-col mt-14 xl:mt-4 2xl:mt-20 h-[500px] sm:h-[700px] xl:h-[800px] 2xl:h-[900px] behind_div'>
        </div>
      </div>
    );
  };
  
  return renderContent();
};

export default Example;

//   const handleThumbsUpClick = async () => {
//     try {
//       await fetchData();
//       console.log('Response:', response);
//     } catch (error) {
//       console.error("Error fetching data:", error);
//     }
//   };
