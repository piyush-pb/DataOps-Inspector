# DataOps Inspector - Vercel Deployment Guide

This guide will help you deploy your DataOps Inspector application to Vercel.

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **GitHub/GitLab Account**: Your code should be in a Git repository
3. **PostgreSQL Database**: You'll need a PostgreSQL database (recommended: Supabase, Railway, or Neon)

## Step 1: Database Setup

### Option A: Supabase (Recommended)
1. Go to [supabase.com](https://supabase.com) and create a new project
2. Get your database connection string from Settings > Database
3. Note down the connection string for later use

### Option B: Railway
1. Go to [railway.app](https://railway.app) and create a new project
2. Add a PostgreSQL database
3. Get the connection string from the database service

### Option C: Neon
1. Go to [neon.tech](https://neon.tech) and create a new project
2. Get your connection string from the dashboard

## Step 2: Prepare Your Repository

1. **Push your code to GitHub/GitLab**:
```bash
git add .
git commit -m "Prepare for Vercel deployment"
git push origin main
```

2. **Ensure all files are committed**:
   - `vercel.json` (root)
   - `package.json` (root)
   - `frontend/package.json`
   - `backend/requirements.txt`
   - All source code files

## Step 3: Deploy to Vercel

### Method 1: Vercel CLI (Recommended)

1. **Install Vercel CLI**:
```bash
npm i -g vercel
```

2. **Login to Vercel**:
```bash
vercel login
```

3. **Deploy from your project directory**:
```bash
vercel
```

4. **Follow the prompts**:
   - Link to existing project? → No
   - Project name → `dataops-inspector` (or your preferred name)
   - Directory → `./` (root directory)
   - Override settings? → No

### Method 2: Vercel Dashboard

1. Go to [vercel.com/dashboard](https://vercel.com/dashboard)
2. Click "New Project"
3. Import your Git repository
4. Configure the project settings:
   - Framework Preset: Other
   - Root Directory: `./`
   - Build Command: `npm run build`
   - Output Directory: `frontend/build`

## Step 4: Environment Variables

In your Vercel project dashboard, go to Settings > Environment Variables and add:

### Required Variables:
```
DATABASE_URL=postgresql://username:password@host:port/database
SECRET_KEY=your-super-secret-key-here
```

### Optional Variables:
```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

## Step 5: Database Migration

After deployment, you'll need to run database migrations. You can do this by:

1. **Accessing your deployed API**:
   - Go to your Vercel deployment URL
   - Navigate to `/docs` to see the FastAPI documentation
   - The database tables should be created automatically on first request

2. **Or manually trigger**:
   - Visit `https://your-app.vercel.app/health` to initialize the database

## Step 6: Verify Deployment

1. **Check Frontend**: Visit your Vercel URL
2. **Check Backend**: Visit `https://your-app.vercel.app/docs`
3. **Test API**: Try the health endpoint at `/health`

## Troubleshooting

### Common Issues:

1. **Build Failures**:
   - Check the build logs in Vercel dashboard
   - Ensure all dependencies are in `package.json` and `requirements.txt`
   - Verify Node.js version compatibility

2. **Database Connection Issues**:
   - Verify your `DATABASE_URL` is correct
   - Ensure your database allows external connections
   - Check if your database service is active

3. **CORS Issues**:
   - The CORS configuration should handle Vercel domains automatically
   - If you have issues, check the browser console for CORS errors

4. **Environment Variables**:
   - Ensure all required environment variables are set in Vercel
   - Variables are case-sensitive
   - Redeploy after adding new environment variables

### Debugging:

1. **Check Vercel Logs**:
   - Go to your project dashboard
   - Click on "Functions" to see serverless function logs
   - Check "Deployments" for build logs

2. **Local Testing**:
   - Test your API locally with the same environment variables
   - Use `vercel dev` to test locally with Vercel configuration

## Post-Deployment

### Custom Domain (Optional):
1. Go to your Vercel project settings
2. Add your custom domain
3. Configure DNS records as instructed

### Monitoring:
1. Set up Vercel Analytics (optional)
2. Monitor your application performance
3. Set up alerts for any issues

### Updates:
To update your deployment:
```bash
git add .
git commit -m "Update message"
git push origin main
```
Vercel will automatically redeploy on push to your main branch.

## Support

If you encounter issues:
1. Check the Vercel documentation
2. Review the build logs
3. Test locally with `vercel dev`
4. Contact Vercel support if needed

## Notes

- The ML pipeline service is not deployed on Vercel (it requires persistent storage)
- For production use, consider using a dedicated backend service like Railway or Heroku
- Vercel is optimized for frontend applications and serverless functions
- Database operations should be lightweight for optimal performance 