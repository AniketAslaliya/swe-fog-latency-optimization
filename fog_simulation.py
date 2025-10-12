"""
Fog Computing Simulation Environment
===================================

This module establishes the foundational structure for a fog computing simulation
using Python and SimPy. It defines the core network components and their relationships.

Author: Fog Computing Simulation Team
Date: 2024
"""

import simpy
import random
import math
from typing import List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class DeviceType(Enum):
    """Enumeration for different types of network devices."""
    IOT_DEVICE = "iot_device"
    FOG_NODE = "fog_node"
    CLOUD_SERVER = "cloud_server"


@dataclass
class Location:
    """Represents a 2D location in the simulation environment."""
    x: float
    y: float
    
    def distance_to(self, other: 'Location') -> float:
        """Calculate Euclidean distance to another location."""
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)


@dataclass
class ComputationalResources:
    """Represents computational resources of a device."""
    cpu_mips: float  # Million Instructions Per Second
    memory: float    # Memory in MB
    storage: float   # Storage in MB
    
    def __str__(self):
        return f"CPU: {self.cpu_mips} MIPS, Memory: {self.memory} MB, Storage: {self.storage} MB"


class IoTDevice:
    """
    Represents an IoT device in the fog computing network.
    
    IoT devices generate tasks and are connected to fog nodes for processing.
    They have limited computational resources and rely on fog/cloud for heavy processing.
    """
    
    def __init__(self, device_id: str, location: Location, 
                 computational_resources: ComputationalResources,
                 fog_node: Optional['FogNode'] = None):
        """
        Initialize an IoT device.
        
        Args:
            device_id: Unique identifier for the device
            location: Physical location of the device
            computational_resources: Available computational resources
            fog_node: Connected fog node for task processing
        """
        self.device_id = device_id
        self.location = location
        self.computational_resources = computational_resources
        self.connected_fog_node = fog_node
        self.device_type = DeviceType.IOT_DEVICE
        
        # Task generation parameters
        self.task_generation_rate = random.uniform(0.1, 0.5)  # Tasks per second
        self.task_size_range = (1, 10)  # MB
        
    def __str__(self):
        return f"IoT Device {self.device_id} at {self.location} -> Fog Node {self.connected_fog_node.node_id if self.connected_fog_node else 'None'}"
    
    def get_nearest_fog_node(self, fog_nodes: List['FogNode']) -> 'FogNode':
        """Find the nearest fog node to this IoT device."""
        if not fog_nodes:
            raise ValueError("No fog nodes available")
        
        nearest_fog = min(fog_nodes, key=lambda fog: self.location.distance_to(fog.location))
        return nearest_fog


class FogNode:
    """
    Represents a fog node in the fog computing network.
    
    Fog nodes provide intermediate processing capabilities between IoT devices
    and the cloud server. They have moderate computational resources and can
    offload tasks to the cloud when necessary.
    """
    
    def __init__(self, node_id: str, location: Location, 
                 computational_resources: ComputationalResources,
                 cloud_server: Optional['CloudServer'] = None):
        """
        Initialize a fog node.
        
        Args:
            node_id: Unique identifier for the fog node
            location: Physical location of the fog node
            computational_resources: Available computational resources
            cloud_server: Reference to the central cloud server
        """
        self.node_id = node_id
        self.location = location
        self.computational_resources = computational_resources
        self.connected_cloud_server = cloud_server
        self.device_type = DeviceType.FOG_NODE
        
        # SimPy resource for processing capacity
        self.processing_capacity = None  # Will be set by the simulation environment
        self.connected_iot_devices: List[IoTDevice] = []
        
        # Performance metrics
        self.tasks_processed = 0
        self.tasks_offloaded = 0
        
    def __str__(self):
        return f"Fog Node {self.node_id} at {self.location} with {self.computational_resources}"
    
    def add_iot_device(self, iot_device: IoTDevice):
        """Add an IoT device to this fog node's network."""
        iot_device.connected_fog_node = self
        self.connected_iot_devices.append(iot_device)
    
    def get_utilization(self) -> float:
        """Calculate current resource utilization."""
        if self.processing_capacity:
            return 1.0 - (self.processing_capacity.capacity - self.processing_capacity.count) / self.processing_capacity.capacity
        return 0.0


class CloudServer:
    """
    Represents the central cloud server in the fog computing network.
    
    The cloud server has significantly more computational resources than fog nodes
    and can handle complex tasks that cannot be processed at the fog level.
    """
    
    def __init__(self, server_id: str, location: Location, 
                 computational_resources: ComputationalResources):
        """
        Initialize a cloud server.
        
        Args:
            server_id: Unique identifier for the cloud server
            location: Physical location of the cloud server
            computational_resources: Available computational resources
        """
        self.server_id = server_id
        self.location = location
        self.computational_resources = computational_resources
        self.device_type = DeviceType.CLOUD_SERVER
        
        # SimPy resource for processing capacity
        self.processing_capacity = None  # Will be set by the simulation environment
        
        # Performance metrics
        self.tasks_processed = 0
        self.total_processing_time = 0.0
        
    def __str__(self):
        return f"Cloud Server {self.server_id} at {self.location} with {self.computational_resources}"


class FogComputingSimulation:
    """
    Main simulation environment for fog computing scenarios.
    
    This class manages the overall simulation, including the network topology,
    component initialization, and simulation execution.
    """
    
    def __init__(self, simulation_time: float = 1000.0):
        """
        Initialize the fog computing simulation environment.
        
        Args:
            simulation_time: Total simulation time in seconds
        """
        self.env = simpy.Environment()
        self.simulation_time = simulation_time
        
        # Network components
        self.cloud_server: Optional[CloudServer] = None
        self.fog_nodes: List[FogNode] = []
        self.iot_devices: List[IoTDevice] = []
        
        # Simulation metrics
        self.start_time = 0
        self.end_time = 0
        
    def create_network_topology(self, num_fog_nodes: int = 3, num_iot_devices: int = 10):
        """
        Create the network topology with cloud server, fog nodes, and IoT devices.
        
        Args:
            num_fog_nodes: Number of fog nodes to create
            num_iot_devices: Number of IoT devices to create
        """
        print("🌐 Creating Fog Computing Network Topology...")
        print("=" * 50)
        
        # Create cloud server (centralized, high resources)
        self.cloud_server = CloudServer(
            server_id="CLOUD_001",
            location=Location(50, 50),  # Center of the simulation area
            computational_resources=ComputationalResources(
                cpu_mips=10000,  # 10,000 MIPS
                memory=32000,    # 32 GB
                storage=1000000   # 1 TB
            )
        )
        
        # Create fog nodes (distributed, moderate resources)
        fog_locations = [
            Location(20, 20), Location(80, 20), Location(50, 80)
        ]
        
        for i in range(num_fog_nodes):
            fog_node = FogNode(
                node_id=f"FOG_{i+1:03d}",
                location=fog_locations[i] if i < len(fog_locations) else Location(
                    random.uniform(10, 90), random.uniform(10, 90)
                ),
                computational_resources=ComputationalResources(
                    cpu_mips=random.uniform(1000, 3000),  # 1,000-3,000 MIPS
                    memory=random.uniform(4000, 8000),    # 4-8 GB
                    storage=random.uniform(100000, 500000)  # 100-500 GB
                ),
                cloud_server=self.cloud_server
            )
            self.fog_nodes.append(fog_node)
        
        # Create IoT devices (distributed, limited resources)
        for i in range(num_iot_devices):
            iot_device = IoTDevice(
                device_id=f"IOT_{i+1:03d}",
                location=Location(
                    random.uniform(5, 95), random.uniform(5, 95)
                ),
                computational_resources=ComputationalResources(
                    cpu_mips=random.uniform(50, 200),   # 50-200 MIPS
                    memory=random.uniform(256, 1024),  # 256 MB - 1 GB
                    storage=random.uniform(1000, 10000)  # 1-10 GB
                )
            )
            
            # Connect to nearest fog node
            nearest_fog = iot_device.get_nearest_fog_node(self.fog_nodes)
            nearest_fog.add_iot_device(iot_device)
            self.iot_devices.append(iot_device)
    
    def initialize_simpy_resources(self):
        """Initialize SimPy resources for processing capacity modeling."""
        print("\n🔧 Initializing SimPy Resources...")
        
        # Cloud server processing capacity (high)
        self.cloud_server.processing_capacity = simpy.Resource(
            self.env, capacity=10
        )
        
        # Fog nodes processing capacity (moderate)
        for fog_node in self.fog_nodes:
            capacity = max(2, int(fog_node.computational_resources.cpu_mips / 1000))
            fog_node.processing_capacity = simpy.Resource(
                self.env, capacity=capacity
            )
    
    def print_network_summary(self):
        """Print a comprehensive summary of the created network."""
        print("\n📊 Network Topology Summary")
        print("=" * 50)
        
        # Cloud server info
        print(f"\n☁️  Cloud Server:")
        print(f"   ID: {self.cloud_server.server_id}")
        print(f"   Location: {self.cloud_server.location}")
        print(f"   Resources: {self.cloud_server.computational_resources}")
        print(f"   Processing Capacity: {self.cloud_server.processing_capacity.capacity}")
        
        # Fog nodes info
        print(f"\n🌫️  Fog Nodes ({len(self.fog_nodes)}):")
        for i, fog_node in enumerate(self.fog_nodes, 1):
            print(f"   {i}. {fog_node.node_id}")
            print(f"      Location: {fog_node.location}")
            print(f"      Resources: {fog_node.computational_resources}")
            print(f"      Processing Capacity: {fog_node.processing_capacity.capacity}")
            print(f"      Connected IoT Devices: {len(fog_node.connected_iot_devices)}")
        
        # IoT devices info
        print(f"\n📱 IoT Devices ({len(self.iot_devices)}):")
        for i, iot_device in enumerate(self.iot_devices, 1):
            print(f"   {i}. {iot_device.device_id}")
            print(f"      Location: {iot_device.location}")
            print(f"      Resources: {iot_device.computational_resources}")
            print(f"      Connected to: {iot_device.connected_fog_node.node_id}")
        
        # Network statistics
        print(f"\n📈 Network Statistics:")
        print(f"   Total Devices: {len(self.iot_devices) + len(self.fog_nodes) + 1}")
        print(f"   Average IoT devices per fog node: {len(self.iot_devices) / len(self.fog_nodes):.1f}")
        
        # Calculate network coverage
        total_fog_capacity = sum(fog.processing_capacity.capacity for fog in self.fog_nodes)
        cloud_capacity = self.cloud_server.processing_capacity.capacity
        print(f"   Total Fog Processing Capacity: {total_fog_capacity}")
        print(f"   Cloud Processing Capacity: {cloud_capacity}")
        print(f"   Fog-to-Cloud Capacity Ratio: {total_fog_capacity / cloud_capacity:.2f}")
    
    def run_simulation(self):
        """Run the simulation for the specified duration."""
        print(f"\n🚀 Starting Simulation for {self.simulation_time} seconds...")
        print("=" * 50)
        
        self.start_time = self.env.now
        self.env.run(until=self.simulation_time)
        self.end_time = self.env.now
        
        print(f"✅ Simulation completed in {self.end_time - self.start_time:.2f} seconds")
    
    def setup_simulation(self, num_fog_nodes: int = 3, num_iot_devices: int = 10):
        """Complete setup of the simulation environment."""
        print("🔧 Setting up Fog Computing Simulation Environment")
        print("=" * 60)
        
        # Create network topology
        self.create_network_topology(num_fog_nodes, num_iot_devices)
        
        # Initialize SimPy resources
        self.initialize_simpy_resources()
        
        # Print network summary
        self.print_network_summary()
        
        print(f"\n✅ Simulation environment setup complete!")
        print(f"   Ready to run simulation for {self.simulation_time} seconds")


def main():
    """Main function to demonstrate the fog computing simulation setup."""
    print("🌐 Fog Computing Simulation Environment")
    print("=" * 60)
    print("Setting up core network components and topology...")
    
    # Create simulation environment
    simulation = FogComputingSimulation(simulation_time=100.0)
    
    # Setup the simulation with default parameters
    simulation.setup_simulation(
        num_fog_nodes=3,
        num_iot_devices=10
    )
    
    # Run the simulation
    simulation.run_simulation()
    
    print("\n🎉 Simulation setup and execution completed successfully!")
    print("Next steps: Add task generation and processing logic.")


if __name__ == "__main__":
    main()
