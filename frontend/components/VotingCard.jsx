"use client";
import { useState } from "react";

const VotingCard = ({ response, onThumbsUpClick }) => {
  const [thumbsUp, setThumbsUp] = useState(false);

  const handleThumbsUpClick = () => {
    setThumbsUp(true);
    onThumbsUpClick();
  };

  return (
    <div className="voting_card">
      <p className="my-4 font-satoshi text-sm text-gray-700">{response}</p>

      <div className="flex justify-center items-center mt-5">
        <button
          onClick={handleThumbsUpClick}
          className={`thumbs_up_btn ${thumbsUp ? 'thumbs_up_btn_active' : ''}`}
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-6 w-6"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M5 15l7-7 7 7"
            />
          </svg>
        </button>
      </div>
    </div>
  );
};

export default VotingCard;
