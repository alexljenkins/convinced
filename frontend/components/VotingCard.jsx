"use client";
import { useState, useEffect } from "react";

const VotingCard = ({ content, fetcher }) => {

  console.log(content);
  const [thumbsUp, setThumbsUp] = useState(false);

  const handleThumbsUpClick = () => {
    // console.log('thumbs up clicked');
    setThumbsUp(true);
    // wait 1 second
    setTimeout(() => {
      setThumbsUp(false);
      fetcher();
    }, 1000);
  };

  return (
    <div className="voting_card cursor-pointer" onClick={handleThumbsUpClick}>
      
      <p className="my-4 font-satoshi text-sm text-white">{JSON.stringify(content['user_input'])}</p>
      {thumbsUp ? (
        <div className='flex-center flex-col'>
          <p className='ai_response text-center flex-col'> +{JSON.stringify(content['if_wins'])} points</p>
        </div>
        ) : (
          <div></div>
        )}
    </div>
  );
};

export default VotingCard;
