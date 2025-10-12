# Fog Computing Simulation Environment

A comprehensive Python-based simulation environment for fog computing scenarios using SimPy discrete-event simulation framework.

## 🌐 Overview

This simulation environment models a fog computing network with three main components:
- **IoT Devices**: Generate tasks and have limited computational resources
- **Fog Nodes**: Provide intermediate processing capabilities with moderate resources
- **Cloud Server**: Centralized high-performance computing with extensive resources

## 🏗️ Architecture

### Core Components

#### IoTDevice Class
- **Purpose**: Represents IoT devices that generate computational tasks
- **Attributes**: 
  - `device_id`: Unique identifier
  - `location`: 2D coordinates in simulation space
  - `computational_resources`: CPU, memory, and storage capacity
  - `connected_fog_node`: Reference to assigned fog node
- **Capabilities**: Task generation, nearest fog node discovery

#### FogNode Class
- **Purpose**: Intermediate processing nodes between IoT devices and cloud
- **Attributes**:
  - `node_id`: Unique identifier
  - `location`: Physical position in simulation space
  - `computational_resources`: Processing capacity (moderate)
  - `connected_cloud_server`: Reference to central cloud
  - `processing_capacity`: SimPy Resource for concurrent processing
- **Capabilities**: Task processing, cloud offloading, IoT device management

#### CloudServer Class
- **Purpose**: Centralized high-performance computing resource
- **Attributes**:
  - `server_id`: Unique identifier
  - `location`: Physical position (typically center of network)
  - `computational_resources`: High-capacity processing resources
  - `processing_capacity`: SimPy Resource for concurrent processing
- **Capabilities**: Heavy computational tasks, centralized processing

### Network Topology

The simulation establishes a hierarchical network structure:

```
IoT Devices → Fog Nodes → Cloud Server
     ↓           ↓           ↓
  Limited    Moderate    High Resources
 Resources   Resources   Resources
```

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```python
from fog_simulation import FogComputingSimulation

# Create simulation environment
simulation = FogComputingSimulation(simulation_time=100.0)

# Setup network topology
simulation.setup_simulation(
    num_fog_nodes=3,
    num_iot_devices=10
)

# Run simulation
simulation.run_simulation()
```

### Running the Simulation

```bash
python fog_simulation.py
```

## 📊 Simulation Features

### Network Initialization
- **Automatic Topology Creation**: Generates fog nodes and IoT devices with realistic distributions
- **Resource Assignment**: Assigns computational resources based on device type
- **Connection Management**: Establishes IoT-to-fog and fog-to-cloud connections
- **Load Balancing**: Distributes IoT devices to nearest fog nodes

### Resource Modeling
- **CPU Capacity**: Modeled in MIPS (Million Instructions Per Second)
- **Memory**: Modeled in MB/GB
- **Storage**: Modeled in MB/GB
- **Processing Capacity**: SimPy Resources for concurrent task processing

### Performance Metrics
- **Resource Utilization**: Tracks CPU, memory, and processing capacity usage
- **Network Coverage**: Analyzes device distribution and connectivity
- **Load Distribution**: Monitors task distribution across fog nodes
- **Processing Statistics**: Tracks tasks processed and offloaded

## 🔧 Configuration

### Simulation Parameters

```python
# Simulation duration
simulation_time = 1000.0  # seconds

# Network topology
num_fog_nodes = 3         # Number of fog nodes
num_iot_devices = 10      # Number of IoT devices

# Resource specifications
cloud_resources = ComputationalResources(
    cpu_mips=10000,       # 10,000 MIPS
    memory=32000,         # 32 GB
    storage=1000000       # 1 TB
)

fog_resources = ComputationalResources(
    cpu_mips=2000,        # 2,000 MIPS
    memory=6000,          # 6 GB
    storage=300000        # 300 GB
)

iot_resources = ComputationalResources(
    cpu_mips=100,         # 100 MIPS
    memory=512,           # 512 MB
    storage=5000          # 5 GB
)
```

## 📈 Output and Visualization

### Network Summary
The simulation provides detailed information about:
- Device locations and connections
- Resource allocations and capacities
- Network topology statistics
- Performance metrics and utilization

### Example Output
```
🌐 Creating Fog Computing Network Topology...
==================================================

☁️  Cloud Server:
   ID: CLOUD_001
   Location: Location(x=50, y=50)
   Resources: CPU: 10000 MIPS, Memory: 32000 MB, Storage: 1000000 MB
   Processing Capacity: 10

🌫️  Fog Nodes (3):
   1. FOG_001
      Location: Location(x=20, y=20)
      Resources: CPU: 2500 MIPS, Memory: 6000 MB, Storage: 300000 MB
      Processing Capacity: 2
      Connected IoT Devices: 3

📱 IoT Devices (10):
   1. IOT_001
      Location: Location(x=15, y=18)
      Resources: CPU: 150 MIPS, Memory: 512 MB, Storage: 5000 MB
      Connected to: FOG_001
```

## 🔮 Future Enhancements

This foundational structure supports future additions:
- **Task Generation**: Implement task creation and scheduling
- **Processing Logic**: Add task processing algorithms
- **Offloading Strategies**: Implement fog-to-cloud offloading decisions
- **Performance Analysis**: Add detailed metrics and visualization
- **Network Dynamics**: Model network failures and recovery
- **Energy Consumption**: Add power consumption modeling

## 📚 Dependencies

- **SimPy**: Discrete-event simulation framework
- **NumPy**: Numerical computing
- **Pandas**: Data manipulation and analysis
- **Matplotlib/Seaborn**: Visualization (optional)
- **tqdm**: Progress bars

## 🤝 Contributing

This simulation environment is designed to be extensible. Key areas for contribution:
- Additional network topologies
- Advanced resource modeling
- Performance optimization
- Visualization enhancements
- Documentation improvements

## 📄 License

This project is part of the fog computing simulation research initiative.
