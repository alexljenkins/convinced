"use client"
import VotingCard from "@components/VotingCard";
import { fetchReviewData } from '@components/api/ReviewData';
import { useState, useEffect } from 'react';

const reviewPage = () => {
  const [cardcontent, setCardContent] = useState({ 'response': [{ 'user_input': 'Sending message to space' }, {'user_input': 'Please Wait...'}]});
  
  const fetchCardContent = async () => {
    const data = await fetchReviewData();
    setCardContent(data);
  };

  useEffect(() => {
    if (cardcontent.response[0].user_input === 'Sending message to space') {
      fetchCardContent();
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
          If you were an alien, which of these messages<br />
          is more likely to convince you to let Earth live?
        </p>
        <div className="container pt-14 px-2 lg:px-4 lg:mx-auto">
          <div className="grid gap-4 lg:grid-cols-2 grid-cols-1 text-white">
            <div>
              <VotingCard content={cardcontent['response'][0]} other_id={parseInt(cardcontent['response'][1]['response_id'])} fetcher={fetchCardContent} />
            </div>
            <div>
              <VotingCard content={cardcontent['response'][1]} other_id={parseInt(cardcontent['response'][0]['response_id'])} fetcher = {fetchCardContent} />
            </div>
          </div>
        </div>
      </div>
    );
  };
  
  return renderContent();
};

export default reviewPage;