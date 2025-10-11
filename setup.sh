#!/bin/bash

echo "🚀 Setting up Fog Simulator..."

echo ""
echo "📝 Creating environment file..."
cat > client/.env.local << EOF
VITE_FOG_FUNCTION_URL=http://127.0.0.1:5001/swe-fog-latency-optimization/us-central1/processOnFog
VITE_CLOUD_FUNCTION_URL=http://127.0.0.1:5001/swe-fog-latency-optimization/us-central1/processOnCloud
VITE_FIREBASE_API_KEY=AIzaSyAzi8DED5WbwVaGToSd5ZxMx4btP5oUcLY
VITE_FIREBASE_AUTH_DOMAIN=swe-fog-latency-optimization.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=swe-fog-latency-optimization
VITE_FIREBASE_STORAGE_BUCKET=swe-fog-latency-optimization.firebasestorage.app
VITE_FIREBASE_MESSAGING_SENDER_ID=702224469157
VITE_FIREBASE_APP_ID=1:702224469157:web:d8530ce92499dd125d514c
EOF

echo ""
echo "📦 Installing backend dependencies..."
cd functions
npm install
if [ $? -ne 0 ]; then
    echo "❌ Failed to install backend dependencies"
    exit 1
fi
cd ..

echo ""
echo "📦 Installing frontend dependencies..."
cd client
npm install
if [ $? -ne 0 ]; then
    echo "❌ Failed to install frontend dependencies"
    exit 1
fi
cd ..

echo ""
echo "✅ Setup completed successfully!"
echo ""
echo "🚀 To run the application:"
echo "1. Terminal 1: firebase emulators:start"
echo "2. Terminal 2: cd client && npm run dev"
echo "3. Open: http://localhost:5173"
echo ""
echo "📖 See DEPLOYMENT_GUIDE.md for detailed instructions"
