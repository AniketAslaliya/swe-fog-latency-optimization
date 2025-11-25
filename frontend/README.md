# Fog Computing Simulator - Frontend

React + Tailwind CSS frontend for the fog computing simulation platform.

## 🚀 Quick Start

### Installation

```bash
cd frontend
npm install
```

### Running the Development Server

```bash
npm run dev
```

The frontend will start on **http://localhost:3000**

## 📦 Building for Production

```bash
npm run build
```

Built files will be in the `dist` directory.

## 🔗 Backend Connection

The frontend automatically connects to the backend API at `http://localhost:5000` via Vite proxy.

Make sure the backend is running before starting the frontend!

## 🛠️ Technologies

- React 18
- Vite
- Tailwind CSS
- Chart.js
- Firebase (Authentication)

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/     # React components
│   ├── hooks/          # Custom React hooks
│   ├── App.jsx         # Main app component
│   ├── firebase.js     # Firebase configuration
│   └── main.jsx        # Entry point
├── index.html
├── package.json
└── vite.config.js
```

## 🔧 Configuration

- **Port**: 3000 (configured in `vite.config.js`)
- **API Proxy**: Automatically proxies `/api/*` to `http://localhost:5000`


