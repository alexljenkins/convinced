"use client";
import { useState, useEffect } from "react";

const VotingCard = ({ content, fetcher }) => {

  console.log(content);
  const [thumbsUp, setThumbsUp] = useState(false);

  const handleThumbsUpClick = () => {
    // console.log('thumbs up clicked');
    setThumbsUp(true);
    fetcher();
  };

  return (
    <div className="voting_card cursor-pointer" onClick={handleThumbsUpClick}>
      
      <p className="my-4 font-satoshi text-sm text-white">{content}</p>

      {/* <div className="flex justify-center items-center mt-5"> */}
        {/* <button
          onClick={handleThumbsUpClick}
          className={`thumbs_up_btn ${thumbsUp ? 'thumbs_up_btn_active' : ''}`}
        >
        </button> */}
      {/* </div> */}
    </div>
  );
};

export default VotingCard;
