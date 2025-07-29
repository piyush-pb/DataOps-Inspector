// Test script to check specific API endpoint
const testUrl = 'https://data-ops-inspector.vercel.app/api/v1/dashboard/overview';

console.log('Testing specific API endpoint...\n');

fetch(testUrl)
  .then(response => {
    console.log(`Status: ${response.status}`);
    console.log(`Headers:`, response.headers);
    return response.text();
  })
  .then(text => {
    console.log(`Response (first 300 chars):`);
    console.log(text.substring(0, 300));
  })
  .catch(error => {
    console.log(`Error: ${error.message}`);
  }); 