# 🚀 Complete Deployment Guide

## 📋 Prerequisites
- Node.js 18+ installed
- Firebase CLI installed (`npm install -g firebase-tools`)
- Git installed
- Vercel account (for production deployment)

## 🏠 Local Development Setup

### Step 1: Create Environment File
Create `client/.env.local` with the following content:

```env
# Local Development Environment Variables
VITE_FOG_FUNCTION_URL=http://127.0.0.1:5001/swe-fog-latency-optimization/us-central1/processOnFog
VITE_CLOUD_FUNCTION_URL=http://127.0.0.1:5001/swe-fog-latency-optimization/us-central1/processOnCloud

# Firebase Configuration
VITE_FIREBASE_API_KEY=AIzaSyAzi8DED5WbwVaGToSd5ZxMx4btP5oUcLY
VITE_FIREBASE_AUTH_DOMAIN=swe-fog-latency-optimization.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=swe-fog-latency-optimization
VITE_FIREBASE_STORAGE_BUCKET=swe-fog-latency-optimization.firebasestorage.app
VITE_FIREBASE_MESSAGING_SENDER_ID=702224469157
VITE_FIREBASE_APP_ID=1:702224469157:web:d8530ce92499dd125d514c
```

### Step 2: Install Dependencies
```bash
# Install backend dependencies
cd functions
npm install
cd ..

# Install frontend dependencies
cd client
npm install
cd ..
```

### Step 3: Firebase Setup
```bash
# Login to Firebase
firebase login

# Initialize Firebase (if not already done)
firebase init
# Select: Functions, Emulators
# Choose project: swe-fog-latency-optimization
# Use TypeScript for functions
```

### Step 4: Enable Google Authentication
1. Go to [Firebase Console](https://console.firebase.google.com)
2. Select project: `swe-fog-latency-optimization`
3. Go to Authentication → Sign-in method
4. Enable Google provider
5. Add `localhost:5173` to authorized domains

### Step 5: Run the Application

#### Terminal 1: Start Firebase Emulators
```bash
firebase emulators:start
```

#### Terminal 2: Start React Development Server
```bash
cd client
npm run dev
```

#### Open Browser
Navigate to `http://localhost:5173`

## ☁️ Production Deployment (Vercel)

### Step 1: Deploy Firebase Functions
```bash
# Deploy backend functions
firebase deploy --only functions
```

After deployment, note the function URLs:
- `https://us-central1-swe-fog-latency-optimization.cloudfunctions.net/processOnFog`
- `https://us-central1-swe-fog-latency-optimization.cloudfunctions.net/processOnCloud`

### Step 2: Deploy Frontend to Vercel

#### Option A: Using Vercel CLI
```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy from project root
vercel

# Follow the prompts:
# - Set up and deploy? Yes
# - Which scope? (your account)
# - Link to existing project? No
# - Project name: swe-fog-simulator
# - Directory: ./
# - Override settings? No
```

#### Option B: Using Vercel Dashboard
1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "Add New... → Project"
3. Import your GitHub repository: `AniketAslaliya/swe-fog-latency-optimization`
4. Configure project:
   - **Framework Preset**: Vite
   - **Root Directory**: `client`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

### Step 3: Configure Environment Variables in Vercel

In Vercel Dashboard → Project Settings → Environment Variables, add:

```env
VITE_FOG_FUNCTION_URL=https://us-central1-swe-fog-latency-optimization.cloudfunctions.net/processOnFog
VITE_CLOUD_FUNCTION_URL=https://us-central1-swe-fog-latency-optimization.cloudfunctions.net/processOnCloud
VITE_FIREBASE_API_KEY=AIzaSyAzi8DED5WbwVaGToSd5ZxMx4btP5oUcLY
VITE_FIREBASE_AUTH_DOMAIN=swe-fog-latency-optimization.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=swe-fog-latency-optimization
VITE_FIREBASE_STORAGE_BUCKET=swe-fog-latency-optimization.firebasestorage.app
VITE_FIREBASE_MESSAGING_SENDER_ID=702224469157
VITE_FIREBASE_APP_ID=1:702224469157:web:d8530ce92499dd125d514c
```

### Step 4: Update Firebase Auth Domains
1. Go to Firebase Console → Authentication → Settings
2. Add your Vercel domain to authorized domains:
   - `your-app-name.vercel.app`
   - `your-app-name-git-main-your-username.vercel.app`

### Step 5: Deploy
```bash
# Deploy to Vercel
vercel --prod
```

## 🔧 Quick Commands

### Local Development
```bash
# Quick setup script
./setup.bat  # Windows
./setup.sh   # Unix/Linux

# Manual setup
echo "VITE_FOG_FUNCTION_URL=http://127.0.0.1:5001/swe-fog-latency-optimization/us-central1/processOnFog" > client/.env.local
echo "VITE_CLOUD_FUNCTION_URL=http://127.0.0.1:5001/swe-fog-latency-optimization/us-central1/processOnCloud" >> client/.env.local
echo "VITE_FIREBASE_API_KEY=AIzaSyAzi8DED5WbwVaGToSd5ZxMx4btP5oUcLY" >> client/.env.local
echo "VITE_FIREBASE_AUTH_DOMAIN=swe-fog-latency-optimization.firebaseapp.com" >> client/.env.local
echo "VITE_FIREBASE_PROJECT_ID=swe-fog-latency-optimization" >> client/.env.local
echo "VITE_FIREBASE_STORAGE_BUCKET=swe-fog-latency-optimization.firebasestorage.app" >> client/.env.local
echo "VITE_FIREBASE_MESSAGING_SENDER_ID=702224469157" >> client/.env.local
echo "VITE_FIREBASE_APP_ID=1:702224469157:web:d8530ce92499dd125d514c" >> client/.env.local

# Install and run
cd functions && npm install && cd ..
cd client && npm install && cd ..
firebase emulators:start  # Terminal 1
cd client && npm run dev  # Terminal 2
```

### Production Deployment
```bash
# Deploy backend
firebase deploy --only functions

# Deploy frontend
vercel --prod
```

## 🐛 Troubleshooting

### Common Issues

1. **Environment variables not loading**:
   - Ensure `.env.local` is in `client` folder
   - Restart development server
   - Check file permissions

2. **Firebase auth not working**:
   - Verify Google provider is enabled
   - Check authorized domains
   - Ensure correct project ID

3. **CORS errors**:
   - Verify emulators are running
   - Check function URLs
   - Ensure proper headers

4. **Build failures**:
   - Check Node.js version (18+)
   - Clear npm cache: `npm cache clean --force`
   - Delete node_modules and reinstall

### Debug Commands
```bash
# Check Firebase project
firebase projects:list

# Check emulator status
firebase emulators:start --debug

# View function logs
firebase functions:log

# Check Vercel deployment
vercel logs
```

## 📊 Expected Results

### Local Development
- **URL**: `http://localhost:5173`
- **Fog Processing**: ~100-200ms latency
- **Cloud Processing**: ~500-600ms latency
- **Performance Difference**: ~400ms faster with fog

### Production Deployment
- **URL**: `https://your-app.vercel.app`
- **Same performance characteristics**
- **Secure authentication**
- **Scalable infrastructure**

## 🎯 Success Indicators

✅ **Local Development**:
- Firebase emulators running on port 5001
- React app running on port 5173
- Google authentication working
- Packet simulation showing latency differences

✅ **Production Deployment**:
- Firebase functions deployed successfully
- Vercel app deployed and accessible
- Environment variables configured
- Authentication working in production

Your fog simulator is now ready for both local development and production deployment! 🚀
