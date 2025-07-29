// Test script to check main alias URL
const testUrls = [
  'https://data-ops-inspector.vercel.app/health',
  'https://data-ops-inspector.vercel.app/api/v1/dashboard/overview',
  'https://data-ops-inspector.vercel.app/'
];

console.log('Testing main alias URLs...\n');

testUrls.forEach(async (url) => {
  try {
    const response = await fetch(url);
    console.log(`✅ ${url}`);
    console.log(`   Status: ${response.status}`);
    if (response.status === 200) {
      const text = await response.text();
      console.log(`   Response (first 200 chars): ${text.substring(0, 200)}`);
    }
    console.log('');
  } catch (error) {
    console.log(`❌ ${url}`);
    console.log(`   Error: ${error.message}\n`);
  }
}); 