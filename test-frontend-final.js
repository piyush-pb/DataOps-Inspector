// Test script to verify frontend is accessible
const frontendUrl = 'https://data-ops-inspector.vercel.app/';

console.log('🌐 Testing DataOps Inspector Frontend...\n');

fetch(frontendUrl)
  .then(response => {
    console.log(`✅ Frontend Status: ${response.status}`);
    console.log(`   Content-Type: ${response.headers.get('content-type')}`);
    
    if (response.status === 200) {
      console.log('🎉 Frontend is accessible and working!');
      console.log('📱 You can now visit: https://data-ops-inspector.vercel.app');
      console.log('🔧 To enable full features, set up a database following DATABASE_SETUP.md');
    } else {
      console.log('⚠️  Frontend might have issues');
    }
  })
  .catch(error => {
    console.log(`❌ Frontend Error: ${error.message}`);
  }); 