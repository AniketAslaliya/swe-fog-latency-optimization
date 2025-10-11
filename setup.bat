@echo off
echo 🚀 Setting up Fog Simulator...

echo.
echo 📝 Creating environment file...
echo VITE_FOG_FUNCTION_URL=http://127.0.0.1:5001/swe-fog-latency-optimization/us-central1/processOnFog > client\.env.local
echo VITE_CLOUD_FUNCTION_URL=http://127.0.0.1:5001/swe-fog-latency-optimization/us-central1/processOnCloud >> client\.env.local
echo VITE_FIREBASE_API_KEY=AIzaSyAzi8DED5WbwVaGToSd5ZxMx4btP5oUcLY >> client\.env.local
echo VITE_FIREBASE_AUTH_DOMAIN=swe-fog-latency-optimization.firebaseapp.com >> client\.env.local
echo VITE_FIREBASE_PROJECT_ID=swe-fog-latency-optimization >> client\.env.local
echo VITE_FIREBASE_STORAGE_BUCKET=swe-fog-latency-optimization.firebasestorage.app >> client\.env.local
echo VITE_FIREBASE_MESSAGING_SENDER_ID=702224469157 >> client\.env.local
echo VITE_FIREBASE_APP_ID=1:702224469157:web:d8530ce92499dd125d514c >> client\.env.local

echo.
echo 📦 Installing backend dependencies...
cd functions
call npm install
if %errorlevel% neq 0 (
    echo ❌ Failed to install backend dependencies
    pause
    exit /b 1
)
cd ..

echo.
echo 📦 Installing frontend dependencies...
cd client
call npm install
if %errorlevel% neq 0 (
    echo ❌ Failed to install frontend dependencies
    pause
    exit /b 1
)
cd ..

echo.
echo ✅ Setup completed successfully!
echo.
echo 🚀 To run the application:
echo 1. Terminal 1: firebase emulators:start
echo 2. Terminal 2: cd client
echo 3. Terminal 2: npm run dev
echo 4. Open: http://localhost:5173
echo.
echo 📖 See DEPLOYMENT_GUIDE.md for detailed instructions
pause
