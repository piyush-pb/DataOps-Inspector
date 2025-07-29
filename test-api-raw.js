// Test script to see raw API response
const testUrl = 'https://data-ops-inspector.vercel.app/api/v1/dashboard/overview';

console.log('Testing raw API response...\n');

fetch(testUrl)
  .then(response => {
    console.log(`Status: ${response.status}`);
    console.log(`Headers:`, response.headers);
    return response.text();
  })
  .then(text => {
    console.log(`Response (first 500 chars):`);
    console.log(text.substring(0, 500));
  })
  .catch(error => {
    console.log(`Error: ${error.message}`);
  }); 