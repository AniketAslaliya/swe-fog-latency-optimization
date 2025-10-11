# Latency-Optimized Fog Architecture Simulator

A modern web application that demonstrates the performance benefits of fog computing over traditional cloud processing. This simulator visually shows how processing IoT data on intermediate "fog nodes" results in lower latency compared to sending all data to a centralized "cloud."

## 🏗️ Architecture

- **Frontend**: React + TypeScript + Vite (deployed on Vercel)
- **Backend**: Firebase Cloud Functions (TypeScript)
- **Purpose**: Demonstrate fog vs cloud processing latency differences

## 🚀 Quick Start

### Prerequisites

- Node.js 18+
- Firebase CLI
- Git

### Local Development

1. **Clone and setup the project:**
   ```bash
   git clone <your-repo-url>
   cd swe-fog-simulator
   ```

2. **Setup Firebase Functions:**
   ```bash
   cd functions
   npm install
   ```

3. **Setup React Client:**
   ```bash
   cd ../client
   npm install
   ```

4. **Configure environment variables:**
   ```bash
   # Copy the example environment file
   cp env.example .env.local
   
   # Edit .env.local with your Firebase project ID
   # Replace 'your-project-id' with your actual Firebase project ID
   ```

5. **Start Firebase emulators:**
   ```bash
   # From the root directory
   firebase emulators:start
   ```

6. **Start the React development server:**
   ```bash
   # In a new terminal, from the client directory
   cd client
   npm run dev
   ```

7. **Open your browser:**
   Navigate to `http://localhost:5173`

## 📦 Deployment

### Step 1: Deploy Backend (Firebase Cloud Functions)

1. **Initialize Firebase (if not already done):**
   ```bash
   firebase login
   firebase init
   ```

2. **Deploy the functions:**
   ```bash
   firebase deploy --only functions
   ```

3. **Copy the production URLs** that Firebase provides for your functions.

### Step 2: Deploy Frontend (Vercel)

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy on Vercel:**
   - Go to [Vercel Dashboard](https://vercel.com/dashboard)
   - Click "Add New... → Project"
   - Import your GitHub repository
   - In "Configure Project", add these environment variables:
     - `VITE_FOG_FUNCTION_URL`: Your Firebase fog function URL
     - `VITE_CLOUD_FUNCTION_URL`: Your Firebase cloud function URL
   - Click "Deploy"

## 🎯 How It Works

### Simulation Logic

1. **Packet Generation**: Creates random data packets with:
   - Random size (0-1000)
   - Random complexity (low/high)

2. **Offloading Decision**: Simple rule-based algorithm:
   - **Fog**: Low complexity AND size < 500
   - **Cloud**: High complexity OR size ≥ 500

3. **Processing Simulation**:
   - **Fog**: 100ms delay (simulates local processing)
   - **Cloud**: 500ms delay (simulates network + cloud processing)

4. **Latency Measurement**: Real-time calculation of round-trip time

### Key Features

- **Real-time Visualization**: Live event log showing processing decisions
- **Performance Comparison**: Clear latency differences between fog and cloud
- **Responsive Design**: Works on desktop and mobile devices
- **Modern UI**: Clean, professional interface with smooth animations

## 🛠️ Development

### Project Structure

```
swe-fog-simulator/
├── functions/                 # Firebase Cloud Functions
│   ├── src/
│   │   └── index.ts          # Cloud Functions code
│   ├── package.json
│   └── tsconfig.json
├── client/                   # React frontend
│   ├── src/
│   │   ├── services/
│   │   │   └── api.ts        # API service
│   │   ├── App.tsx           # Main component
│   │   ├── App.css           # Styles
│   │   └── main.tsx          # Entry point
│   ├── package.json
│   └── vite.config.ts
├── firebase.json             # Firebase configuration
└── README.md
```

### Environment Variables

**Local Development (.env.local):**
```env
VITE_FOG_FUNCTION_URL=http://127.0.0.1:5001/your-project-id/us-central1/processOnFog
VITE_CLOUD_FUNCTION_URL=http://127.0.0.1:5001/your-project-id/us-central1/processOnCloud
```

**Production (Vercel):**
```env
VITE_FOG_FUNCTION_URL=https://us-central1-your-project-id.cloudfunctions.net/processOnFog
VITE_CLOUD_FUNCTION_URL=https://us-central1-your-project-id.cloudfunctions.net/processOnCloud
```

## 🧪 Testing

### Manual Testing

1. Click "Generate and Process Packet" multiple times
2. Observe the latency differences between fog and cloud processing
3. Notice how the offloading algorithm makes decisions based on packet properties

### Expected Results

- **Fog processing**: ~100-200ms total latency
- **Cloud processing**: ~500-600ms total latency
- **Performance difference**: ~400ms faster with fog processing

## 📊 Performance Insights

This simulator demonstrates key fog computing benefits:

1. **Reduced Latency**: Local processing eliminates network round-trips
2. **Smart Offloading**: Only complex/large tasks go to the cloud
3. **Scalability**: Fog nodes can handle high-frequency, low-latency tasks
4. **Efficiency**: Optimal resource utilization based on task characteristics

## 🔧 Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure Firebase functions are deployed and URLs are correct
2. **Environment Variables**: Verify Vercel environment variables are set correctly
3. **Build Failures**: Check that all dependencies are installed

### Debug Mode

Enable detailed logging by opening browser developer tools and monitoring the Network tab during packet processing.

## 📝 License

This project is created for educational and demonstration purposes.

## 🤝 Contributing

Feel free to submit issues and enhancement requests!
