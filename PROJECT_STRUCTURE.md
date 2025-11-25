# 📁 Project Structure

## Overview

The project is now organized into separate **frontend** and **backend** folders for better maintainability and deployment.

```
swe-fog-simulator/
├── frontend/                 # React + Tailwind CSS Frontend
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── hooks/            # Custom React hooks
│   │   ├── App.jsx           # Main app
│   │   ├── firebase.js       # Firebase config
│   │   └── main.jsx          # Entry point
│   ├── index.html            # HTML entry
│   ├── package.json          # Node dependencies
│   ├── vite.config.js        # Vite config (proxies to backend)
│   ├── tailwind.config.js    # Tailwind config
│   └── start.bat             # Windows startup script
│
├── backend/                  # Flask API Backend
│   ├── app.py                # Flask application
│   ├── config.json           # Configuration
│   ├── requirements.txt      # Python dependencies
│   └── start.bat             # Windows startup script
│
├── start.bat                 # Master startup (both servers)
├── start.sh                  # Linux/Mac startup script
└── README_SETUP.md           # Setup instructions
```

## 🔌 Connection Flow

```
Browser (http://localhost:3000)
    ↓
Frontend (React/Vite)
    ↓ (proxies /api/*)
Backend API (http://localhost:5000)
    ↓
Flask REST API
```

## 🚀 Quick Start

### Option 1: Master Script (Easiest)

**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

### Option 2: Manual (Recommended for Development)

**Terminal 1 - Backend:**
```bash
cd backend
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

## 🔧 Port Configuration

| Service | Default Port | Config File |
|---------|-------------|-------------|
| Backend API | 5000 | `backend/app.py` (line 549) |
| Frontend Dev | 3000 | `frontend/vite.config.js` (line 7) |

### Changing Ports

**Backend:**
1. Edit `backend/app.py` line 549
2. Update `frontend/vite.config.js` line 10 to match

**Frontend:**
1. Edit `frontend/vite.config.js` line 7
2. Vite will auto-use next available port if taken

## 📦 Dependencies

### Backend
- Flask 2.3.0+
- Flask-CORS 4.0.0+
- Werkzeug 2.3.0+

### Frontend
- React 18.2.0
- Vite 5.0.8
- Tailwind CSS 3.3.6
- Chart.js 4.4.0
- Firebase 10.7.1

## 🔒 CORS Configuration

Backend CORS is configured in `backend/app.py` line 15:
```python
CORS(app, origins=["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:3000"])
```

Add more origins as needed.

## ✅ Verification Checklist

- [ ] Backend folder exists with `app.py`
- [ ] Frontend folder exists with `src/` directory
- [ ] `backend/config.json` exists
- [ ] `frontend/vite.config.js` proxies to `http://localhost:5000`
- [ ] Both `start.bat` files work
- [ ] Master `start.bat` launches both servers

## 🎯 Next Steps

1. Install dependencies in both folders
2. Start both servers
3. Open http://localhost:3000
4. Test the application!


