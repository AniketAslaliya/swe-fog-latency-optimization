# 🚀 Complete Setup Guide

## Prerequisites
- Node.js 18+ installed
- Firebase CLI installed (`npm install -g firebase-tools`)
- Git installed

## Step 1: Create Environment File

Create a file named `.env.local` in the `client` folder with this exact content:

```env
# For local testing with the Firebase Emulator Suite
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

## Step 2: Install Dependencies

### Backend Dependencies
```bash
cd functions
npm install
cd ..
```

### Frontend Dependencies
```bash
cd client
npm install
cd ..
```

## Step 3: Firebase Setup

### Login to Firebase
```bash
firebase login
```

### Initialize Firebase (if needed)
```bash
firebase init
```
- Select "Functions" and "Emulators"
- Choose your project: `swe-fog-latency-optimization`
- Use TypeScript for functions
- Install dependencies when prompted

### Enable Google Authentication
1. Go to [Firebase Console](https://console.firebase.google.com)
2. Select your project: `swe-fog-latency-optimization`
3. Go to Authentication → Sign-in method
4. Enable Google provider
5. Add `localhost:5173` to authorized domains

## Step 4: Run the Application

### Terminal 1: Start Firebase Emulators
```bash
firebase emulators:start
```
This will start:
- Functions emulator on port 5001
- UI emulator on port 4000

### Terminal 2: Start React Development Server
```bash
cd client
npm run dev
```

## Step 5: Test the Application

1. Open `http://localhost:5173` in your browser
2. Click "Sign in with Google"
3. Complete Google authentication
4. Click "Generate and Process Packet" to test the simulation
5. Observe the latency differences between fog and cloud processing

## Expected Results

- **Fog Processing**: ~100-200ms total latency
- **Cloud Processing**: ~500-600ms total latency
- **Performance Difference**: ~400ms faster with fog processing

## Troubleshooting

### Common Issues

1. **Environment variables not loading**: 
   - Make sure `.env.local` is in the `client` folder
   - Restart the development server

2. **Firebase auth not working**: 
   - Check that Google provider is enabled in Firebase Console
   - Verify authorized domains include `localhost:5173`

3. **CORS errors**: 
   - Ensure Firebase emulators are running
   - Check that function URLs match your project ID

4. **Functions not found**: 
   - Verify Firebase project ID matches in all configs
   - Check that emulators are running on port 5001

### Debug Commands

```bash
# Check Firebase project
firebase projects:list

# Check emulator status
firebase emulators:start --debug

# View function logs
firebase functions:log
```

## Project Structure
```
swe-fog-simulator/
├── functions/                 # Firebase Cloud Functions
│   ├── src/index.ts         # Cloud Functions with auth
│   └── package.json
├── client/                   # React Frontend
│   ├── .env.local           # Environment variables (create this)
│   ├── src/
│   │   ├── config/firebase.ts
│   │   ├── services/auth.ts
│   │   ├── services/api.ts
│   │   └── App.tsx
│   └── package.json
├── firebase.json
└── README.md
```

## Quick Start Commands

```bash
# 1. Create environment file
echo "VITE_FOG_FUNCTION_URL=http://127.0.0.1:5001/swe-fog-latency-optimization/us-central1/processOnFog
VITE_CLOUD_FUNCTION_URL=http://127.0.0.1:5001/swe-fog-latency-optimization/us-central1/processOnCloud
VITE_FIREBASE_API_KEY=AIzaSyAzi8DED5WbwVaGToSd5ZxMx4btP5oUcLY
VITE_FIREBASE_AUTH_DOMAIN=swe-fog-latency-optimization.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=swe-fog-latency-optimization
VITE_FIREBASE_STORAGE_BUCKET=swe-fog-latency-optimization.firebasestorage.app
VITE_FIREBASE_MESSAGING_SENDER_ID=702224469157
VITE_FIREBASE_APP_ID=1:702224469157:web:d8530ce92499dd125d514c" > client/.env.local

# 2. Install dependencies
cd functions && npm install && cd ..
cd client && npm install && cd ..

# 3. Start emulators (Terminal 1)
firebase emulators:start

# 4. Start client (Terminal 2)
cd client && npm run dev
```

## Production Deployment

### Deploy Firebase Functions
```bash
firebase deploy --only functions
```

### Deploy Frontend to Vercel
1. Push code to GitHub
2. Connect repository to Vercel
3. Add environment variables in Vercel dashboard
4. Deploy

The application will demonstrate the clear performance benefits of fog computing over traditional cloud processing!
