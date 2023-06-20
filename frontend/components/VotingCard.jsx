"use client";
import { sendError } from "next/dist/server/api-utils";
import { useState, useEffect, useCallback} from "react";

const VotingCard = ({ content, other_id, fetcher }) => {

  console.log(content);
  const [thumbsUp, setThumbsUp] = useState(false);
  const [showReportButton, setShowReportButton] = useState(false);
  const [showReportOverlay, setShowReportOverlay] = useState(false);

  const sendVote = useCallback(async (winnerId, other_id, ifWinsValue) => {
    console.log('Sending data: ', winnerId, other_id, ifWinsValue);
    try {
      const response = await fetch('http://localhost:8000/api/vote', {
        method: 'POST',
          headers: {'Content-Type': 'application/json',},
          body: JSON.stringify({
            "key": "alexisthebestchuckouttherest",
            "winner_id": winnerId,
            "loser_id": other_id,
            "points_change": ifWinsValue
          }),
        });
      if (response.ok) {
        // Vote sent successfully
        console.log('Vote sent!');
      } else {
        // Handle error case
        console.error('Failed to send vote.');
      }
    } catch (error) {
      console.error('Failed to send vote:', error);
    }
  }, []);

  const handleThumbsUpClick = useCallback(async (winnerId, other_id, ifWinsValue) => {
    console.log('thumbs up clicked');
    console.log(winnerId, other_id, ifWinsValue);
    await sendVote(winnerId, other_id, ifWinsValue);

    setThumbsUp(true);
    // wait 1 second
    setTimeout(() => {
      setThumbsUp(false);
      fetcher();
    }, 1000);
  }, []);

  const handleReportClick = useCallback(async (report_id) => {
    console.log("Report button clicked");
    try {
      const response = await fetch('http://localhost:8000/api/report', {
        method: 'POST',
          headers: {'Content-Type': 'application/json',},
          body: JSON.stringify({
            "key": "alexisthebestchuckouttherest",
            "response_id": report_id
          }),
        });
      if (response.ok) {
        console.log('Report sent!');
      } else {
        // Handle error case
        console.error('Failed report response: ', report_id);
      }
    } catch (error) {
      console.error('Failed to send report. ', error);
    }
    setShowReportOverlay(true);

    setTimeout(() => {
      setShowReportOverlay(false);
      fetcher();
    }, 1500);

  }, []);

return (
    <div
      className="voting_card cursor-pointer relative"
      onMouseEnter={() => setShowReportButton(true)}
      onMouseLeave={() => setShowReportButton(false)}
      onClick={() =>
        handleThumbsUpClick(
          parseInt(content["response_id"]),
          other_id,
          parseInt(content["if_wins"])
        )
      }
    >
      <div className={`${showReportButton ? "block" : "hidden"} absolute top-0 right-0 m-2 z-10`}>
        <button
          className="bg-transparent border-none outline-none focus:outline-none"
          onClick={(e) => {
            e.stopPropagation();
            handleReportClick(content["response_id"]);
          }}
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
      {thumbsUp ? (
        <div className="flex-center flex-col absolute top-0 left-0 right-0 bottom-0 voted_bg">
          <p className="text-center text-white">
            +{JSON.stringify(content["if_wins"])} points
          </p>
        </div>
      ) : null}
        {showReportOverlay && (
          <div className="absolute top-0 left-0 right-0 bottom-0 flex items-center justify-center bg-red-500 font-bold bg-opacity-75 text-white z-20">
            <p className="text-center">Message Reported</p>
          </div>
        )}
    </div>
  );
};

export default VotingCard;
