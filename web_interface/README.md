# Fog Computing Simulator - Web Interface

A modern, interactive web interface for the advanced fog computing simulation platform. This web application provides a comprehensive dashboard for configuring, running, and analyzing fog computing simulations with real-time monitoring and visualization.

## 🌟 Features

### 🎛️ **Interactive Dashboard**
- Real-time simulation status and metrics
- Network topology visualization
- Live activity monitoring
- Performance statistics

### ⚙️ **Configuration Management**
- JSON-based configuration system
- Network topology setup (fog nodes, IoT devices, cloud server)
- Task generation parameters
- Network latency configuration
- Offloading decision parameters

### 🚀 **Simulation Control**
- Start/stop simulations with real-time feedback
- Progress tracking and status monitoring
- Event logging and activity tracking
- Configurable simulation parameters

### 📊 **Advanced Analytics**
- Interactive charts and visualizations
- Performance metrics analysis
- Resource utilization monitoring
- Failure event tracking
- Comparative analysis tools

### 🔧 **Advanced Features**
- Node failure simulation with automatic recovery
- Intelligent task offloading decisions
- Real-time network monitoring
- Comprehensive logging and analytics

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Installation

1. **Navigate to the web interface directory:**
   ```bash
   cd web_interface
   ```

2. **Run the startup script:**
   ```bash
   python start_web.py
   ```

   The script will automatically:
   - Check Python version compatibility
   - Install required dependencies
   - Setup configuration files
   - Start the web server
   - Open the web interface in your browser

3. **Access the web interface:**
   - Open your browser to `http://localhost:5000`
   - The interface will load automatically

### Manual Setup (Alternative)

If you prefer manual setup:

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the server:**
   ```bash
   python app.py
   ```

3. **Open in browser:**
   Navigate to `http://localhost:5000`

## 📱 Interface Overview

### Dashboard Section
- **Quick Stats**: Overview of fog nodes, IoT devices, tasks processed, and average latency
- **Network Topology**: Visual representation of the network structure
- **Recent Activity**: Real-time log of simulation events

### Simulation Section
- **Control Panel**: Configure simulation parameters
- **Status Monitoring**: Real-time simulation status and progress
- **Output Console**: Live simulation output and logging

### Configuration Section
- **Network Tab**: Configure fog nodes, IoT devices, and cloud server
- **Tasks Tab**: Set task generation parameters
- **Latency Tab**: Configure network latency settings
- **Offloading Tab**: Set offloading decision thresholds

### Analytics Section
- **Performance Charts**: Interactive visualizations of simulation results
- **Resource Utilization**: CPU and memory utilization across nodes
- **Failure Analysis**: Comprehensive failure event tracking
- **Performance Summary**: Key performance indicators

### Documentation Section
- **Getting Started**: Quick start guide and tutorials
- **Simulation Basics**: Core concepts and components
- **Configuration Guide**: Detailed configuration options
- **Advanced Features**: Node failures, offloading, monitoring
- **API Reference**: Backend API documentation
- **Future Work**: Planned enhancements and roadmap

## 🔧 Configuration

### Network Topology
```json
{
  "network_topology": {
    "num_fog_nodes": 3,
    "num_iot_devices": 10,
    "cloud_server": {
      "resources": {
        "cpu_mips": 10000,
        "memory_mb": 32000,
        "storage_mb": 1000000
      }
    }
  }
}
```

### Task Generation
```json
{
  "task_generation": {
    "generation_rate_range": [0.1, 0.3],
    "complexity_range": [50, 2000],
    "deadline_range": [5, 30]
  }
}
```

### Offloading Parameters
```json
{
  "offloading_parameters": {
    "complexity_threshold": 1000.0,
    "utilization_threshold": 0.8,
    "deadline_threshold": 5.0,
    "queue_length_threshold": 5
  }
}
```

## 📊 API Endpoints

The web interface communicates with a Flask backend API:

- `GET /api/status` - Get simulation status
- `GET /api/config` - Get current configuration
- `POST /api/config` - Update configuration
- `POST /api/simulation/start` - Start simulation
- `POST /api/simulation/stop` - Stop simulation
- `GET /api/simulation/events` - Get simulation events
- `GET /api/analytics/metrics` - Get performance metrics
- `GET /api/network/topology` - Get network topology
- `GET /api/export/data` - Export simulation data

## 🎨 User Interface

### Modern Design
- **Glassmorphism**: Frosted glass effects with backdrop blur
- **Gradient Backgrounds**: Beautiful color transitions
- **Responsive Layout**: Works on desktop, tablet, and mobile
- **Dark/Light Themes**: Automatic theme detection
- **Smooth Animations**: Fluid transitions and interactions

### Interactive Elements
- **Real-time Updates**: Live data streaming from backend
- **Interactive Charts**: Chart.js-powered visualizations
- **Dynamic Forms**: Responsive configuration forms
- **Status Indicators**: Visual feedback for all operations
- **Notification System**: Toast notifications for user feedback

## 🔬 Advanced Features

### Node Failure Simulation
- Configurable failure probability and duration
- Automatic task rerouting when nodes fail
- Recovery simulation with status tracking
- Failure event logging and analysis

### Intelligent Offloading
- Multi-factor decision engine
- Real-time node utilization monitoring
- Network latency consideration
- Deadline-aware task scheduling

### Performance Monitoring
- Real-time metrics collection
- Resource utilization tracking
- Performance analytics
- Comparative analysis tools

## 🛠️ Development

### Project Structure
```
web_interface/
├── index.html          # Main HTML interface
├── styles.css          # CSS styling and animations
├── script.js           # JavaScript functionality
├── app.py              # Flask backend API
├── start_web.py        # Startup script
├── requirements.txt    # Python dependencies
└── README.md           # This documentation
```

### Backend Integration
The web interface integrates with the Python simulation backend:
- **Configuration Manager**: Centralized config management
- **Enhanced Simulation**: Advanced simulation features
- **Real-time Communication**: WebSocket-like event streaming
- **Data Export**: Comprehensive data export capabilities

### Frontend Technologies
- **HTML5**: Semantic markup and modern features
- **CSS3**: Advanced styling with flexbox and grid
- **JavaScript ES6+**: Modern JavaScript with async/await
- **Chart.js**: Interactive data visualizations
- **Font Awesome**: Icon library for UI elements

## 🚀 Deployment

### Local Development
```bash
python start_web.py
```

### Production Deployment
```bash
# Install production dependencies
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

## 📈 Performance

### Optimization Features
- **Lazy Loading**: Load resources only when needed
- **Caching**: Browser caching for static assets
- **Compression**: Gzip compression for API responses
- **Efficient Updates**: Minimal DOM manipulation
- **Background Processing**: Non-blocking operations

### Browser Compatibility
- **Chrome**: 80+ (Recommended)
- **Firefox**: 75+
- **Safari**: 13+
- **Edge**: 80+

## 🔒 Security

### Security Features
- **CORS Protection**: Cross-origin request security
- **Input Validation**: Server-side validation
- **Error Handling**: Graceful error management
- **Secure Headers**: Security headers for protection

## 📚 Documentation

### User Guide
- **Getting Started**: Quick setup and first simulation
- **Configuration**: Detailed parameter explanation
- **Simulation**: Running and monitoring simulations
- **Analytics**: Understanding results and metrics

### Developer Guide
- **API Documentation**: Complete API reference
- **Extension Guide**: Adding new features
- **Customization**: Modifying the interface
- **Integration**: Connecting with other systems

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Code Style
- **HTML**: Semantic markup with accessibility
- **CSS**: BEM methodology and consistent naming
- **JavaScript**: ES6+ with async/await
- **Python**: PEP 8 compliance

## 📄 License

This project is part of the Fog Computing Simulator platform. See the main project license for details.

## 🆘 Support

### Troubleshooting
- **Check Python version**: Ensure Python 3.8+
- **Verify dependencies**: Run `pip install -r requirements.txt`
- **Check ports**: Ensure port 5000 is available
- **Browser console**: Check for JavaScript errors

### Common Issues
- **CORS errors**: Ensure backend is running
- **Connection refused**: Check if server is started
- **Module not found**: Install missing dependencies
- **Port in use**: Change port in app.py

## 🎯 Future Enhancements

### Planned Features
- **Real-time Collaboration**: Multi-user simulation sessions
- **Advanced Visualizations**: 3D network topology
- **Machine Learning**: ML-based offloading decisions
- **Mobile App**: Native mobile application
- **Cloud Deployment**: AWS/Azure integration

### Roadmap
- **Phase 1**: Core web interface (✅ Complete)
- **Phase 2**: Advanced visualizations
- **Phase 3**: Mobile optimization
- **Phase 4**: Cloud deployment
- **Phase 5**: Enterprise features

---

**🌐 Fog Computing Simulator Web Interface**  
*Advanced platform for fog computing research and analysis*

For more information, visit the main project documentation or contact the development team.
