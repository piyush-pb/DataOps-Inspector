#!/bin/bash

# DataOps Inspector - Vercel Deployment Script

echo "🚀 Starting DataOps Inspector deployment to Vercel..."

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI is not installed. Installing now..."
    npm install -g vercel
fi

# Check if user is logged in to Vercel
if ! vercel whoami &> /dev/null; then
    echo "🔐 Please log in to Vercel..."
    vercel login
fi

# Build the frontend
echo "📦 Building frontend..."
cd frontend
npm install
npm run build
cd ..

# Deploy to Vercel
echo "🚀 Deploying to Vercel..."
vercel --prod

echo "✅ Deployment complete!"
echo "📝 Don't forget to:"
echo "   1. Set up your database (Supabase, Railway, or Neon)"
echo "   2. Add environment variables in Vercel dashboard:"
echo "      - DATABASE_URL"
echo "      - SECRET_KEY"
echo "   3. Test your deployment at the provided URL" 