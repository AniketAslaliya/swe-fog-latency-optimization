# 🚀 Quick Deployment Steps

## Backend on Render (5 minutes)

1. **Go to Render Dashboard** → New → Web Service
2. **Connect GitHub** → Select your repo
3. **Configure:**
   - Name: `fog-computing-backend`
   - Root Directory: `backend`
   - Build: `pip install -r requirements.txt`
   - Start: `python app.py`
4. **Add Environment Variable:**
   - `FRONTEND_URL` = (you'll add this after deploying frontend)
5. **Deploy** → Copy backend URL

## Frontend on Vercel (3 minutes)

1. **Go to Vercel Dashboard** → Add New Project
2. **Import GitHub repo**
3. **Configure:**
   - Root Directory: `frontend`
   - Framework: Vite (auto-detected)
4. **Add Environment Variable:**
   - `VITE_API_URL` = `https://your-backend.onrender.com`
5. **Deploy** → Copy frontend URL

## Update Backend CORS

1. Go back to Render → Your Backend Service
2. Update `FRONTEND_URL` = `https://your-app.vercel.app`
3. Save → Auto-redeploys

## Done! ✅

Your app is live:
- Frontend: `https://your-app.vercel.app`
- Backend: `https://your-backend.onrender.com`

See `DEPLOYMENT_GUIDE.md` for detailed instructions.

