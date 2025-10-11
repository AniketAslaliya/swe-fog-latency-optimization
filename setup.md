# 🚀 Fog Simulator Setup Guide

## Prerequisites
- Node.js 18+ installed
- Firebase CLI installed (`npm install -g firebase-tools`)
- Git installed

## Step-by-Step Setup

### 1. Create Environment File
Create a file named `.env.local` in the `client` folder with the following content:

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

### 2. Install Dependencies

#### Backend (Firebase Functions)
```bash
cd functions
npm install
cd ..
```

#### Frontend (React Client)
```bash
cd client
npm install
cd ..
```

### 3. Firebase Setup

#### Login to Firebase
```bash
firebase login
```

#### Initialize Firebase (if not already done)
```bash
firebase init
```
- Select "Functions" and "Emulators"
- Choose your existing project: `swe-fog-latency-optimization`
- Use TypeScript for functions
- Install dependencies when prompted

#### Enable Google Authentication
1. Go to [Firebase Console](https://console.firebase.google.com)
2. Select your project: `swe-fog-latency-optimization`
3. Go to Authentication → Sign-in method
4. Enable Google provider
5. Add `localhost:5173` to authorized domains for local testing

### 4. Run the Application

#### Start Firebase Emulators
```bash
firebase emulators:start
```
This will start:
- Functions emulator on port 5001
- UI emulator on port 4000

#### Start React Development Server (in a new terminal)
```bash
cd client
npm run dev
```

The application will be available at `http://localhost:5173`

### 5. Test the Application

1. Open `http://localhost:5173` in your browser
2. Click "Sign in with Google"
3. Complete Google authentication
4. Click "Generate and Process Packet" to test the simulation
5. Observe the latency differences between fog and cloud processing

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

## Troubleshooting

### Common Issues

1. **Environment variables not loading**: Make sure `.env.local` is in the `client` folder
2. **Firebase auth not working**: Check that Google provider is enabled in Firebase Console
3. **CORS errors**: Ensure Firebase emulators are running
4. **Functions not found**: Check that Firebase project ID matches in all configs

### Debug Commands

```bash
# Check Firebase project
firebase projects:list

# Check emulator status
firebase emulators:start --debug

# View logs
firebase functions:log
```

## Project Structure
```
swe-fog-simulator/
├── functions/                 # Firebase Cloud Functions
│   ├── src/index.ts         # Cloud Functions with auth
│   └── package.json
├── client/                   # React Frontend
│   ├── src/
│   │   ├── config/firebase.ts
│   │   ├── services/auth.ts
│   │   ├── services/api.ts
│   │   └── App.tsx
│   └── package.json
├── firebase.json
└── README.md
```
