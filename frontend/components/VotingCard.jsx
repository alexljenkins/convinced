"use client";
import { useState, useCallback } from "react";


import { sendVote } from "@components/api/ReviewVote";
import { handleReportClick } from "@components/api/ReviewReport";

const VotingCard = ({ content, other_id, fetcher }) => {
  console.log(content);
  const [busy, setBusy] = useState(false);
  const [showVoteOverlay, setVoteOverlay] = useState(false);
  const [showReportButton, setShowReportButton] = useState(false);
  const [showReportOverlay, setShowReportOverlay] = useState(false);
  

  const handleVote = useCallback(async (winnerId, other_id, ifWinsValue) => {
    if (busy) {
      return; // Exit early if click is already in progress
    }
    setBusy(true);
    setVoteOverlay(true);
    console.log('thumbs up clicked');
    console.log(winnerId, other_id, ifWinsValue);
    await sendVote(winnerId, other_id, ifWinsValue);
    // wait 1 second
    setTimeout(() => {
      fetcher();
      setVoteOverlay(false);
      setBusy(false);
    }, 1000);
  });

  const handleReport = useCallback(async () => {
    if (busy) {
      return; // Exit early if click is already in progress
    }
    setBusy(true);
    setShowReportOverlay(true);
    handleReportClick(content["response_id"]);
    fetcher();
    setTimeout(() => {
      setShowReportOverlay(false);
      setBusy(false);
    }, 1500);
  });

  return (
    <div
      className="voting_card cursor-pointer relative"
      onMouseEnter={() => setShowReportButton(true)}
      onMouseLeave={() => setShowReportButton(false)}
      onClick={(e) => {
        e.stopPropagation();
        handleVote(parseInt(content["response_id"]), other_id, parseInt(content["if_wins"]));
      }}
      disabled={busy}
  >
      <div className={`${showReportButton ? "block" : "hidden"} absolute top-0 right-0 m-2 z-10`}>
        <button
          className="bg-transparent border-none outline-none focus:outline-none"
          onClick={(e) => {
            e.stopPropagation();
            handleReport();
          }}
          disabled={busy}
        >
          <span
            className="text-white cursor-pointer relative z-10"
            title="Report"
            role="img"
            aria-label="Report"
          >
            ❌
          </span>
        </button>
      </div>
      <p className="my-4 font-satoshi text-sm text-white z-10">
        {JSON.stringify(content["user_input"])}
      </p>
      {showVoteOverlay ? (
        <div className="flex-center flex-col absolute top-0 left-0 right-0 bottom-0 voted_bg">
          <p className="text-center text-white">
            +{JSON.stringify(content["if_wins"])} points
          </p>
        </div>
      ) : null}
        {showReportOverlay && (
          <div className="absolute top-0 left-0 right-0 bottom-0 flex items-center justify-center bg-red-500 font-bold bg-opacity-75 text-white z-20">
            <p className="text-center">Message reported. Thank you</p>
          </div>
        )}
    </div>
  );
};

export default VotingCard;
