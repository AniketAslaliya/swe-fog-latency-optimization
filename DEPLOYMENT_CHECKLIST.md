# ✅ Deployment Checklist - Vercel + Render

## 📋 Pre-Deployment Checklist

### Code Changes (✅ DONE)
- [x] All API calls updated to use environment variables
- [x] `vercel.json` configuration files created
- [x] Backend CORS configured for production
- [x] Environment variable support added
- [x] Build tested locally

---

## 🚀 Vercel Deployment Steps

### **CRITICAL: Vercel Settings**

1. **Go to Vercel Dashboard** → Your Project → **Settings** → **General**

2. **Set these EXACT values:**
   ```
   Root Directory: frontend
   Framework Preset: Other (or blank)
   Build Command: npm run build
   Output Directory: dist
   Install Command: npm install
   ```

3. **Go to Settings → Environment Variables**
   - Add: `VITE_API_URL` = `https://your-backend.onrender.com`
   - Select: Production, Preview, Development

4. **Redeploy:**
   - Go to **Deployments** tab
   - Click **"Redeploy"**

---

## 🔧 Render Deployment Steps

1. **Go to Render Dashboard** → **New** → **Web Service**

2. **Connect GitHub** → Select your repo

3. **Configure:**
   ```
   Name: fog-computing-backend
   Root Directory: backend
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: python app.py
   ```

4. **Add Environment Variables:**
   ```
   FRONTEND_URL=https://your-app.vercel.app
   FLASK_ENV=production
   PORT=5000 (auto-set by Render)
   ```

5. **Deploy** → Copy backend URL

6. **Update Vercel:**
   - Go back to Vercel
   - Update `VITE_API_URL` = your Render backend URL
   - Redeploy

---

## ✅ Verification

### Backend:
- Visit: `https://your-backend.onrender.com/api/status`
- Should return JSON ✅

### Frontend:
- Visit: `https://your-app.vercel.app`
- Should load app ✅
- Check browser console for errors

---

## 🐛 Common Issues

### Vercel 404:
- ✅ Root Directory = `frontend`
- ✅ Output Directory = `dist`
- ✅ `VITE_API_URL` is set

### CORS Errors:
- ✅ `FRONTEND_URL` in Render = your Vercel URL
- ✅ No trailing slashes in URLs

### API Not Working:
- ✅ `VITE_API_URL` in Vercel = your Render URL
- ✅ Backend is running on Render

---

## 📝 Quick Reference

**Vercel Settings:**
- Root: `frontend`
- Output: `dist`
- Env Var: `VITE_API_URL`

**Render Settings:**
- Root: `backend`
- Env Var: `FRONTEND_URL`

