# 🚀 Complete Setup Guide

## Project Structure

```
swe-fog-simulator/
├── frontend/          # React + Tailwind CSS frontend
│   ├── src/           # React source code
│   ├── package.json   # Node.js dependencies
│   └── vite.config.js # Vite configuration
├── backend/           # Flask API backend
│   ├── app.py         # Flask application
│   ├── config.json    # Configuration file
│   └── requirements.txt # Python dependencies
└── README_SETUP.md    # This file
```

## 📋 Prerequisites

- **Node.js 18+** ([Download](https://nodejs.org))
- **Python 3.8+** ([Download](https://python.org))
- **npm** (comes with Node.js)

## 🚀 Quick Start

### Step 1: Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Install Frontend Dependencies

```bash
cd frontend
npm install
```

### Step 3: Start Backend Server

**Terminal 1:**
```bash
cd backend
python app.py
```

You should see:
```
🌐 Starting Fog Computing Simulator Backend API
📡 API Server: http://localhost:5000
```

**✅ Keep this terminal open!**

### Step 4: Start Frontend Server

**Terminal 2:**
```bash
cd frontend
npm run dev
```

You should see:
```
  VITE v5.x.x  ready in xxx ms
  ➜  Local:   http://localhost:3000/
```

**✅ Keep this terminal open!**

### Step 5: Open Browser

Navigate to: **http://localhost:3000**

## 🎯 What's Running?

| Service | Port | URL | Purpose |
|---------|------|-----|---------|
| **Backend API** | 5000 | http://localhost:5000 | Flask REST API |
| **Frontend** | 3000 | http://localhost:3000 | React application |

The frontend automatically proxies `/api/*` requests to the backend.

## 🛑 Stopping Servers

Press `Ctrl+C` in each terminal to stop:
1. Stop backend first
2. Then stop frontend

## 🐛 Troubleshooting

### Port 5000 Already in Use

**Windows:**
```bash
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**Or change port in `backend/app.py` (line 549):**
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

Then update `frontend/vite.config.js`:
```javascript
target: 'http://localhost:5001'
```

### Port 3000 Already in Use

Vite will automatically use the next available port. Check the terminal output.

### Module Not Found

**Backend:**
```bash
cd backend
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

### CORS Errors

Make sure:
1. Backend is running on port 5000
2. Frontend is running on port 3000
3. CORS is enabled in `backend/app.py`

## 📝 Development Workflow

1. **Start backend** (Terminal 1)
2. **Start frontend** (Terminal 2)
3. **Make changes** - React auto-reloads, Flask requires restart
4. **Test in browser** at http://localhost:3000

## 🏗️ Production Build

### Build Frontend

```bash
cd frontend
npm run build
```

This creates a `dist` folder with optimized files.

### Serve Production Build

You can serve the `dist` folder with any static file server (nginx, Apache, etc.) and configure it to proxy `/api/*` requests to your backend.

## ✅ Quick Test Checklist

- [ ] Backend running on port 5000
- [ ] Frontend running on port 3000
- [ ] Can access http://localhost:3000
- [ ] Login page loads
- [ ] Can sign up/login
- [ ] Dashboard displays
- [ ] Can start simulation
- [ ] Real-time updates work

## 🎉 You're All Set!

Your separated frontend and backend are now running and connected!


