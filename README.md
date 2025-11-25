# Fog Computing Simulator

A modern web application that demonstrates the performance benefits of fog computing over traditional cloud processing. This simulator visually shows how processing IoT data on intermediate "fog nodes" results in lower latency compared to sending all data to a centralized "cloud."

## 🏗️ Architecture

- **Frontend**: React + Tailwind CSS + Vite
- **Backend**: Flask REST API
- **Purpose**: Demonstrate fog vs cloud processing latency differences

## 🚀 Quick Start

### Prerequisites

- **Node.js 18+** ([Download](https://nodejs.org))
- **Python 3.8+** ([Download](https://python.org))
- **npm** (comes with Node.js)

### Installation & Running

1. **Install Backend Dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Install Frontend Dependencies:**
   ```bash
   cd frontend
   npm install
   ```

3. **Start Both Servers:**

   **Option A: Master Script (Easiest)**
   ```bash
   # Windows
   start.bat
   
   # Linux/Mac
   chmod +x start.sh
   ./start.sh
   ```

   **Option B: Manual (Recommended for Development)**
   
   Terminal 1 - Backend:
   ```bash
   cd backend
   python app.py
   ```
   
   Terminal 2 - Frontend:
   ```bash
   cd frontend
   npm run dev
   ```

4. **Open Browser:**
   Navigate to **http://localhost:3000**

## 📁 Project Structure

```
swe-fog-simulator/
├── frontend/          # React + Tailwind CSS frontend
│   ├── src/           # React source code
│   └── package.json   # Node dependencies
├── backend/           # Flask API backend
│   ├── app.py         # Flask application
│   └── requirements.txt # Python dependencies
└── README_SETUP.md    # Detailed setup guide
```

## 🎯 Features

- **Real-time Simulation**: Live fog computing simulation with configurable parameters
- **Interactive Dashboard**: Visual network topology and performance metrics
- **Analytics**: Comprehensive charts and performance analysis
- **Configuration Management**: Easy-to-use configuration interface
- **IoT Device Management**: Add and manage IoT devices
- **Firebase Authentication**: Secure user authentication

## 🔧 Configuration

- **Backend Port**: 5000 (configured in `backend/app.py`)
- **Frontend Port**: 3000 (configured in `frontend/vite.config.js`)
- **API Proxy**: Frontend automatically proxies `/api/*` to backend

## 📚 Documentation

- **README_SETUP.md** - Complete setup and troubleshooting guide
- **PROJECT_STRUCTURE.md** - Detailed project structure
- **frontend/README.md** - Frontend-specific documentation
- **backend/README.md** - Backend API documentation

## 🛠️ Development

### Making Changes

- **Frontend**: Changes auto-reload (Vite HMR)
- **Backend**: Restart Flask server after Python changes

### Building for Production

```bash
cd frontend
npm run build
```

This creates optimized files in the `dist` folder.

## 🐛 Troubleshooting

See **README_SETUP.md** for detailed troubleshooting guide.

Common issues:
- Port conflicts: Check if ports 5000 or 3000 are in use
- Module errors: Run `npm install` and `pip install -r requirements.txt`
- CORS errors: Ensure both servers are running

## 📝 License

This project is created for educational and demonstration purposes.

## 🤝 Contributing

Feel free to submit issues and enhancement requests!
