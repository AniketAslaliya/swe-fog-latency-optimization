# Fog Computing Simulator - Backend API

Flask REST API server for the fog computing simulation platform.

## 🚀 Quick Start

### Installation

```bash
cd backend
pip install -r requirements.txt
```

### Running the Server

```bash
python app.py
```

The API server will start on **http://localhost:5000**

## 📡 API Endpoints

### Status & Configuration
- `GET /api/status` - Get simulation status
- `GET /api/config` - Get current configuration
- `POST /api/config` - Update configuration

### Simulation Control
- `POST /api/simulation/start` - Start simulation
- `POST /api/simulation/stop` - Stop simulation
- `GET /api/simulation/events` - Get simulation events

### Analytics
- `GET /api/analytics/metrics` - Get performance metrics
- `GET /api/network/topology` - Get network topology
- `GET /api/export/data` - Export simulation data

## ⚙️ Configuration

Configuration is stored in `config.json` and can be updated via the API.

## 🔧 Port Configuration

Default port: **5000**

To change the port, edit `app.py` line 549:
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

## 🔒 CORS

CORS is enabled for:
- `http://localhost:3000` (Vite dev server)
- `http://localhost:5173` (Alternative React dev server)
- `http://127.0.0.1:3000`

To add more origins, edit `app.py` line 15.


