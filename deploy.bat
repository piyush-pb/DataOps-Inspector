@echo off
echo 🚀 Starting DataOps Inspector deployment to Vercel...

REM Check if Vercel CLI is installed
vercel --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Vercel CLI is not installed. Installing now...
    npm install -g vercel
)

REM Check if user is logged in to Vercel
vercel whoami >nul 2>&1
if errorlevel 1 (
    echo 🔐 Please log in to Vercel...
    vercel login
)

REM Build the frontend
echo 📦 Building frontend...
cd frontend
call npm install
call npm run build
cd ..

REM Deploy to Vercel
echo 🚀 Deploying to Vercel...
vercel --prod

echo ✅ Deployment complete!
echo 📝 Don't forget to:
echo    1. Set up your database (Supabase, Railway, or Neon)
echo    2. Add environment variables in Vercel dashboard:
echo       - DATABASE_URL
echo       - SECRET_KEY
echo    3. Test your deployment at the provided URL

pause 