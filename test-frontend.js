// Test script to check frontend
const testUrl = 'https://data-ops-inspector-n7eyvsis4-piyush-pbs-projects.vercel.app/';

console.log('Testing frontend...\n');

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