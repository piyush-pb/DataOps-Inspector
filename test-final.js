// Final test script to verify API endpoints
const testUrls = [
  'https://data-ops-inspector.vercel.app/health',
  'https://data-ops-inspector.vercel.app/api/v1/dashboard/overview',
  'https://data-ops-inspector.vercel.app/api/v1/dashboard/system-status'
];

console.log('Testing DataOps Inspector API endpoints...\n');

testUrls.forEach(async (url) => {
  try {
    const response = await fetch(url);
    const data = await response.json();
    console.log(`✅ ${url}`);
    console.log(`   Status: ${response.status}`);
    console.log(`   Response: ${JSON.stringify(data, null, 2)}\n`);
  } catch (error) {
    console.log(`❌ ${url}`);
    console.log(`   Error: ${error.message}\n`);
  }
}); 