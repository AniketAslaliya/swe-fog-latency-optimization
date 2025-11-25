# 🚀 Deployment Guide - Vercel (Frontend) + Render (Backend)

This guide will help you deploy the Fog Computing Simulator to production.

## 📋 Prerequisites

1. **GitHub Account** - Your code should be pushed to GitHub
2. **Vercel Account** - Sign up at [vercel.com](https://vercel.com)
3. **Render Account** - Sign up at [render.com](https://render.com)

---

## 🔧 Part 1: Deploy Backend to Render

### Step 1: Create Render Web Service

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Select the repository: `swe-fog-latency-optimization`

### Step 2: Configure Backend Service

**Basic Settings:**
- **Name**: `fog-computing-backend` (or any name you prefer)
- **Region**: Choose closest to your users
- **Branch**: `main`
- **Root Directory**: `backend` (important!)

**Build & Deploy:**
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python app.py`

**Environment Variables:**
Click **"Advanced"** → **"Add Environment Variable"** and add:
```
FLASK_ENV=production
PORT=5000
FRONTEND_URL=https://your-vercel-app.vercel.app
```
*(Replace `your-vercel-app` with your actual Vercel domain - you'll get this after deploying frontend)*

### Step 3: Deploy

1. Click **"Create Web Service"**
2. Wait for deployment to complete (5-10 minutes)
3. Copy your backend URL (e.g., `https://fog-computing-backend.onrender.com`)

**Important Notes:**
- Free tier services on Render spin down after 15 minutes of inactivity
- First request after spin-down may take 30-60 seconds
- Consider upgrading to paid plan for always-on service

---

## 🎨 Part 2: Deploy Frontend to Vercel

### Step 1: Create Vercel Project

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click **"Add New..."** → **"Project"**
3. Import your GitHub repository: `swe-fog-latency-optimization`

### Step 2: Configure Frontend Project

**Project Settings:**
- **Framework Preset**: Vite
- **Root Directory**: `frontend` (important!)
- **Build Command**: `npm run build` (auto-detected)
- **Output Directory**: `dist` (auto-detected)

**Environment Variables:**
Click **"Environment Variables"** and add:
```
VITE_API_URL=https://your-backend-app.onrender.com
```
*(Replace `your-backend-app.onrender.com` with your actual Render backend URL)*

### Step 3: Deploy

1. Click **"Deploy"**
2. Wait for deployment (2-5 minutes)
3. Your app will be live at `https://your-app.vercel.app`

### Step 4: Update Backend CORS

After getting your Vercel URL, go back to Render:

1. Go to your backend service settings
2. Update the `FRONTEND_URL` environment variable:
   ```
   FRONTEND_URL=https://your-app.vercel.app
   ```
3. Click **"Save Changes"** - Render will automatically redeploy

---

## 🔄 Part 3: Update Environment Variables

### Backend (Render) - Update These:

1. Go to Render Dashboard → Your Backend Service → **"Environment"**
2. Update/Add:
   ```
   FRONTEND_URL=https://your-vercel-app.vercel.app
   FLASK_ENV=production
   PORT=5000
   ```

### Frontend (Vercel) - Update These:

1. Go to Vercel Dashboard → Your Project → **"Settings"** → **"Environment Variables"**
2. Add/Update:
   ```
   VITE_API_URL=https://your-backend-app.onrender.com
   ```
3. **Important**: After adding/updating, trigger a new deployment:
   - Go to **"Deployments"** tab
   - Click **"..."** on latest deployment → **"Redeploy"**

---

## ✅ Verification Steps

1. **Check Backend:**
   - Visit: `https://your-backend.onrender.com/api/status`
   - Should return JSON with simulation status

2. **Check Frontend:**
   - Visit: `https://your-app.vercel.app`
   - Should load the application
   - Check browser console for any API errors

3. **Test Full Flow:**
   - Start a simulation
   - Check if queue lengths update
   - Verify analytics charts load

---

## 🐛 Troubleshooting

### Backend Issues:

**Problem**: Backend returns 500 errors
- **Solution**: Check Render logs → **"Logs"** tab
- Common issues: Missing environment variables, import errors

**Problem**: CORS errors in browser
- **Solution**: Ensure `FRONTEND_URL` in Render matches your Vercel URL exactly
- Check backend logs for CORS-related errors

**Problem**: Backend times out
- **Solution**: Free tier services spin down after inactivity
- First request after spin-down takes longer (30-60 seconds)

### Frontend Issues:

**Problem**: Can't connect to backend
- **Solution**: 
  1. Verify `VITE_API_URL` is set correctly in Vercel
  2. Ensure backend URL doesn't have trailing slash
  3. Check browser console for exact error

**Problem**: Build fails on Vercel
- **Solution**: 
  1. Check build logs in Vercel dashboard
  2. Ensure `package.json` has all dependencies
  3. Verify Node.js version compatibility

**Problem**: API calls fail
- **Solution**: 
  1. Check if `VITE_API_URL` environment variable is set
  2. Verify backend is running and accessible
  3. Check CORS configuration in backend

---

## 📝 Quick Reference

### Backend URL Format:
```
https://your-service-name.onrender.com
```

### Frontend URL Format:
```
https://your-project-name.vercel.app
```

### Environment Variables Summary:

**Render (Backend):**
- `FRONTEND_URL` - Your Vercel frontend URL
- `FLASK_ENV=production`
- `PORT=5000` (auto-set by Render)

**Vercel (Frontend):**
- `VITE_API_URL` - Your Render backend URL

---

## 🎉 Success!

Once deployed, your application will be:
- **Frontend**: Live on Vercel
- **Backend**: Live on Render
- **Fully Functional**: All features working in production

Share your deployed URLs and enjoy your live application! 🚀

