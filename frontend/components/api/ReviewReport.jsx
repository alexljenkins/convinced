import { fetchApiKey } from '@components/keys';

export const handleReportClick = async (report_id) => {
  console.log("Report button clicked");
  const apiKey = fetchApiKey();
  try {
    const response = await fetch('http://localhost:8000/api/report', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': apiKey,
      },
        body: JSON.stringify({
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
};
