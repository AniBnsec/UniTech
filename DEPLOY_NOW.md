# 🚀 Deploy ThreatShield - Step by Step Guide

Your code is now on GitHub: **https://github.com/AniBnsec/UniTech.git**

## Deployment Options

### Option 1: Vercel + Render (Recommended - Easiest)

This is the fastest way to deploy your application for free.

---

## 📦 Part 1: Deploy Frontend to Vercel

### Step 1: Sign up for Vercel
1. Go to https://vercel.com/signup
2. Sign up with your GitHub account

### Step 2: Import Project
1. Click "Add New Project"
2. Select "Import Git Repository"
3. Choose **AniBnsec/UniTech**
4. Click "Import"

### Step 3: Configure Build Settings
```
Framework Preset: Next.js
Root Directory: frontend
Build Command: npm run build
Output Directory: .next
Install Command: npm install
```

### Step 4: Add Environment Variables
Click "Environment Variables" and add:

```
NEXT_PUBLIC_API_URL = https://your-backend-url.onrender.com
```

(We'll get the backend URL in the next step)

### Step 5: Deploy
- Click "Deploy"
- Wait 2-3 minutes
- Your frontend will be live at: **https://your-project.vercel.app**

---

## 🔧 Part 2: Deploy Backend to Render

### Step 1: Sign up for Render
1. Go to https://render.com/register
2. Sign up with your GitHub account

### Step 2: Create PostgreSQL Database
1. Click "New +" → "PostgreSQL"
2. Name: `threatshield-db`
3. Database: `threat_intel`
4. User: `postgres`
5. Region: Choose closest to you
6. Plan: **Free**
7. Click "Create Database"
8. **Copy the "Internal Database URL"** - you'll need this!

### Step 3: Create Web Service
1. Click "New +" → "Web Service"
2. Connect your GitHub account
3. Select **AniBnsec/UniTech** repository
4. Configure:
   - Name: `threatshield-api`
   - Region: Same as your database
   - Branch: `main`
   - Root Directory: `backend`
   - Runtime: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Plan: **Free**

### Step 4: Add Environment Variables

Click "Environment" tab and add these:

```bash
DATABASE_URL = <paste your Internal Database URL from Step 2>
JWT_SECRET = <generate a random string - use https://randomkeygen.com/>
JWT_ALGORITHM = HS256
JWT_EXPIRATION = 86400
APP_ENV = production
DEBUG = False
CORS_ORIGINS = https://your-project.vercel.app
```

### Step 5: Deploy
- Click "Create Web Service"
- Wait 3-5 minutes for deployment
- Your backend will be live at: **https://threatshield-api.onrender.com**

### Step 6: Initialize Database
1. In Render dashboard, go to your web service
2. Click "Shell" tab
3. Run these commands:
```bash
python -c "from app.database import Base, engine; from app.models import *; Base.metadata.create_all(bind=engine); print('Database initialized!')"
```

---

## 🔄 Part 3: Update Frontend with Backend URL

1. Go back to Vercel dashboard
2. Go to your project → Settings → Environment Variables
3. Update `NEXT_PUBLIC_API_URL` to your Render backend URL:
   ```
   NEXT_PUBLIC_API_URL = https://threatshield-api.onrender.com
   ```
4. Go to Deployments tab
5. Click the three dots (•••) on latest deployment
6. Click "Redeploy"

---

## ✅ Verify Deployment

### Test Backend
Visit: `https://threatshield-api.onrender.com/health`

Should return:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "production"
}
```

### Test Frontend
1. Visit: `https://your-project.vercel.app`
2. Click "Sign Up"
3. Create an account
4. Test URL scanner with: `https://google.com`

---

## 🎯 Your Live URLs

After deployment, you'll have:

- **Frontend**: https://your-project.vercel.app
- **Backend API**: https://threatshield-api.onrender.com
- **API Docs**: https://threatshield-api.onrender.com/docs
- **GitHub**: https://github.com/AniBnsec/UniTech

---

## 🐛 Troubleshooting

### Frontend shows "Network Error"
- Check CORS_ORIGINS in Render includes your Vercel URL
- Restart Render web service

### Backend not starting
- Check Environment Variables are set correctly
- View logs in Render dashboard
- Make sure DATABASE_URL is the Internal URL

### Database connection error
- Go to Render dashboard → PostgreSQL
- Copy "Internal Database URL" (not External)
- Update DATABASE_URL in web service
- Restart service

### Free tier limitations
- Render free tier spins down after 15 minutes of inactivity
- First request after sleep takes ~30 seconds
- Upgrade to paid tier ($7/month) for always-on service

---

## 💰 Cost Breakdown

### Free Tier (Perfect for demo/portfolio)
- Vercel: Free (100GB bandwidth)
- Render Web Service: Free (750 hours/month)
- Render PostgreSQL: Free (90 days, then $7/month)
- **Total: FREE for 90 days**

### Paid Tier (Production-ready)
- Vercel Pro: $20/month
- Render Starter: $7/month (web service)
- Render PostgreSQL: $7/month
- **Total: ~$34/month**

---

## 🎓 Post-Deployment Checklist

- [ ] Frontend loads successfully
- [ ] Can register new account
- [ ] Can login
- [ ] URL scanner works
- [ ] Message scanner works
- [ ] TLS analyzer works
- [ ] Dashboard shows statistics
- [ ] API documentation accessible
- [ ] Database persists data
- [ ] GitHub repository is public

---

## 🔐 Security Checklist for Production

- [ ] Change JWT_SECRET to a strong random value
- [ ] Update CORS_ORIGINS to your actual domain
- [ ] Keep .env files out of git (already in .gitignore)
- [ ] Enable HTTPS (Vercel/Render do this automatically)
- [ ] Set DEBUG = False in production
- [ ] Regular database backups (Render provides this)
- [ ] Monitor error logs regularly

---

## 🎉 Share Your Project

Once deployed, share your work:

### LinkedIn Post Example:
```
🚀 Excited to share my latest project: ThreatShield!

An AI-powered cybersecurity platform that combines:
✅ URL threat detection
✅ Scam message analysis
✅ TLS certificate validation
✅ Blockchain verification

Tech Stack:
- Frontend: Next.js, TypeScript, Tailwind CSS
- Backend: FastAPI, Python, PostgreSQL
- Blockchain: Solidity, Ethereum

Try it live: [your-vercel-url]
GitHub: https://github.com/AniBnsec/UniTech

#Cybersecurity #WebDevelopment #AI #Blockchain
```

---

## 📞 Need Help?

1. Check Render logs: Dashboard → Your Service → Logs
2. Check Vercel logs: Dashboard → Deployments → View Function Logs
3. Test API directly: Visit `/docs` endpoint
4. Review environment variables match exactly

---

**Congratulations! Your cybersecurity platform is now live! 🎉**

Make sure to test all features and share your achievement!
