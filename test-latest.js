// Test script for the latest deployment
const testUrls = [
  'https://data-ops-inspector.vercel.app/health',
  'https://data-ops-inspector.vercel.app/api/v1/dashboard/overview',
  'https://data-ops-inspector.vercel.app/api/v1/dashboard/system-status'
];

console.log('🎉 Testing Latest DataOps Inspector Deployment...\n');

async function testEndpoint(url) {
  try {
    const response = await fetch(url);
    const data = await response.json();
    console.log(`✅ ${url}`);
    console.log(`   Status: ${response.status}`);
    console.log(`   Response: ${JSON.stringify(data, null, 2)}\n`);
    return true;
  } catch (error) {
    console.log(`❌ ${url}`);
    console.log(`   Error: ${error.message}\n`);
    return false;
  }
}

async function runTests() {
  const results = await Promise.all(testUrls.map(testEndpoint));
  const successCount = results.filter(Boolean).length;
  console.log(`📊 Test Results: ${successCount}/${testUrls.length} endpoints working`);
  
  if (successCount === testUrls.length) {
    console.log('🎉 All tests passed! Your DataOps Inspector is fully operational!');
  } else {
    console.log('⚠️  Some endpoints need attention. Check the errors above.');
  }
}

runTests(); 