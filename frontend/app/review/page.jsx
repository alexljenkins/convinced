"use client"
import VotingCard from "@components/VotingCard";

import { useState, useEffect} from 'react';
// import VotingCard from "@components/VotingCard";
// import GetToVoteOnData from "@components/GetToVoteOnData";

// import EarthCanvas from "@components/canvas/Earth";

const Review = () => {
  // const [submitting, setSubmitting] = useState(false);
  const [response, setResponse] = useState([0,0]);

  useEffect(() => {
    // Fetch initial data
    fetchData();
  }, [1, 1]);

  const fetchData = async () => {
    console.log("Getting data because of use effect called.");
    const [error, setError] = useState("");
    // e.preventDefault();
    setError("");
    
    const [key, setKey] = useState("alexisthebestchuckouttherest");
    try {
        const apiResponse = await fetch('http://localhost:8000/api/collect_responses', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ key }),
        });
  
        if (apiResponse.ok) {
          const data = await apiResponse.json();
          DisplayVotingData(data.response)
          console.log('Response received from backend:', data);
          return data;
        } else {
          // Handle the error response
          console.error('Request failed with status:', response.status);
        }
      } catch (error) {
      console.error('An error occurred:', error);
      return ["error", "error"];
      }
    };

  const handleThumbsUpClick = async () => {
    console.log("Getting data because of thumbs up press.");
    try {
      const data = await fetchData();
      setResponse(data);
    } catch (error) {
      console.error("Error fetching data:", error);
      return ["error", "error"];
    }
  };

  return (
    <div className='w-full flex-center flex-col 2xl:mt-10 stacked_containers'>
      <h1 className='head_text orange_gradient text-center top_content'>
        Would you let Earth live?
      </h1>
      <p className='flex-center flex-col py-0 mt-2 sm:mt-0 xl:mt-5 bottom_spacing'></p>
        {/* <div className='flex-center flex-col mt-8 lg:mt-10 xl:mt-20 2xl:mb-24 bottom_spacing'></div> */}
          <p className='desc text-center flex-col top_content'>
            If you were the alien, recieving these messages<br />
            which one would you be more likely to let live?
          </p>
      {/* <div className='flex-center flex-col mt-8 lg:mt-10 xl:mt-20 2xl:mb-24 bottom_spacing'></div> */}
      <div className="container mx-auto px-4">
        <div className="grid gap-4 md:grid-cols-2">
          <div>
            <VotingCard response={response[0]} onThumbsUpClick={handleThumbsUpClick}/>
          </div>
          <div>
            <VotingCard response={response[1]} onThumbsUpClick={handleThumbsUpClick}/>
          </div>
        </div>
      </div>
      <div className='w-full flex-center flex-col mt-14 xl:mt-4 2xl:mt-20 h-[500px] sm:h-[700px] xl:h-[800px] 2xl:h-[900px] behind_div'>
        {/* <EarthCanvas /> */}
      </div>
  </div>
  );
};

export default Review;


