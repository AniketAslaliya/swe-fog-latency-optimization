# 🔧 Vercel 404 Error - Fix Guide

## Problem
Getting `404: NOT_FOUND` error when accessing your Vercel deployment.

## Solution

### Step 1: Update Vercel Project Settings

1. Go to your Vercel project dashboard
2. Click on **"Settings"** → **"General"**
3. Verify these settings:
   - **Framework Preset**: `Vite` (or leave blank)
   - **Root Directory**: `frontend` ✅
   - **Build Command**: `npm run build` ✅
   - **Output Directory**: `dist` ✅
   - **Install Command**: `npm install` ✅

### Step 2: Check Environment Variables

1. Go to **"Settings"** → **"Environment Variables"**
2. Make sure `VITE_API_URL` is set to your Render backend URL
3. Format: `https://your-backend.onrender.com` (no trailing slash)

### Step 3: Redeploy

1. Go to **"Deployments"** tab
2. Click **"..."** on the latest deployment
3. Select **"Redeploy"**
4. Wait for build to complete

### Step 4: Verify Build Output

After deployment, check the build logs:
1. Go to **"Deployments"** → Click on the deployment
2. Check **"Build Logs"**
3. Verify:
   - ✅ `npm run build` completes successfully
   - ✅ `dist` folder is created
   - ✅ `index.html` exists in `dist` folder

### Alternative: Manual Configuration

If automatic detection doesn't work, manually set in Vercel:

**Build & Development Settings:**
```
Framework Preset: Other
Build Command: cd frontend && npm run build
Output Directory: frontend/dist
Install Command: cd frontend && npm install
Root Directory: (leave empty or set to frontend)
```

**Or use Root Directory approach:**
```
Root Directory: frontend
Build Command: npm run build
Output Directory: dist
```

## Common Issues

### Issue 1: Root Directory Not Set
- **Symptom**: Vercel can't find `package.json`
- **Fix**: Set Root Directory to `frontend` in project settings

### Issue 2: Build Output Not Found
- **Symptom**: 404 on all routes
- **Fix**: Verify Output Directory is `dist` (not `frontend/dist`)

### Issue 3: SPA Routing Not Working
- **Symptom**: Works on `/` but 404 on other routes
- **Fix**: `vercel.json` rewrites should handle this (already configured)

## Quick Fix Checklist

- [ ] Root Directory set to `frontend`
- [ ] Build Command: `npm run build`
- [ ] Output Directory: `dist`
- [ ] `vercel.json` exists in `frontend` folder
- [ ] Environment variable `VITE_API_URL` is set
- [ ] Redeployed after making changes

## Still Not Working?

1. **Check Build Logs**: Look for errors during build
2. **Verify File Structure**: Ensure `frontend/dist/index.html` exists after build
3. **Test Locally**: Run `npm run build` in `frontend` folder and check if `dist` folder is created
4. **Contact Support**: If still failing, check Vercel documentation or support

