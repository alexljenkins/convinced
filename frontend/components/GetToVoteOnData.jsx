"use client"
import { useState } from "react";

const GetToVoteOnData = async () => {
  const [error, setError] = useState("");
  // e.preventDefault();
  // setError(""); // Reset the error state
  
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

export default GetToVoteOnData;
