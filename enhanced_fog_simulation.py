"""
Enhanced Fog Computing Simulation with Advanced Features
=======================================================

This module extends the basic fog simulation with configuration management,
node failure simulation, and advanced robustness features.
"""

import simpy
import random
import math
import time
import json
from typing import List, Optional, Tuple, Dict, Any
from dataclasses import dataclass
from enum import Enum

# Import base classes and configuration
from fog_simulation import (
    Location, ComputationalResources, Task, TaskStatus, DeviceType,
    OffloadDecision, PerformanceLogger, global_logger,
    IoTDevice, FogNode, CloudServer, FogComputingSimulation
)
from config_manager import ConfigManager


class NodeStatus(Enum):
    """Enumeration for node operational status."""
    OPERATIONAL = "operational"
    FAILED = "failed"
    RECOVERING = "recovering"


@dataclass
class NodeFailure:
    """Represents a node failure event."""
    node_id: str
    failure_time: float
    recovery_time: float
    failure_duration: float
    failure_type: str = "hardware_failure"


class EnhancedFogNode(FogNode):
    """
    Enhanced Fog Node with failure simulation and recovery capabilities.
    """
    
    def __init__(self, node_id: str, location: Location, 
                 computational_resources: ComputationalResources,
                 cloud_server: 'CloudServer', env: simpy.Environment,
                 config_manager: ConfigManager):
        super().__init__(node_id, location, computational_resources, cloud_server, env)
        self.config_manager = config_manager
        self.status = NodeStatus.OPERATIONAL
        self.failure_history: List[NodeFailure] = []
        self.current_failure: Optional[NodeFailure] = None
        
        # Load configuration parameters
        offload_config = config_manager.get_offloading_config()
        self.complexity_threshold = offload_config.complexity_threshold
        self.utilization_threshold = offload_config.utilization_threshold
        self.deadline_threshold = offload_config.deadline_threshold
        self.queue_length_threshold = offload_config.queue_length_threshold
    
    def simulate_failure(self, failure_time: float, failure_duration: float):
        """
        Simulate a node failure.
        
        Args:
            failure_time: When the failure occurs
            failure_duration: How long the failure lasts
        """
        if self.status == NodeStatus.OPERATIONAL:
            self.status = NodeStatus.FAILED
            self.current_failure = NodeFailure(
                node_id=self.node_id,
                failure_time=failure_time,
                recovery_time=failure_time + failure_duration,
                failure_duration=failure_duration
            )
            self.failure_history.append(self.current_failure)
            
            print(f"💥 {self.node_id}: Node failure at {failure_time:.2f}s (duration: {failure_duration:.2f}s)")
            
            # Clear pending tasks (they will be rerouted)
            self.pending_tasks.clear()
    
    def recover_from_failure(self, recovery_time: float):
        """
        Recover from a node failure.
        
        Args:
            recovery_time: When the recovery occurs
        """
        if self.status == NodeStatus.FAILED and self.current_failure:
            self.status = NodeStatus.OPERATIONAL
            self.current_failure = None
            
            print(f"🔧 {self.node_id}: Node recovered at {recovery_time:.2f}s")
    
    def is_operational(self) -> bool:
        """Check if the node is operational."""
        return self.status == NodeStatus.OPERATIONAL
    
    def receive_task(self, task: Task):
        """
        Enhanced task receiving with failure handling.
        
        Args:
            task: The task to be processed
        """
        if not self.is_operational():
            print(f"❌ {self.node_id}: Node is down, cannot receive task {task.task_id}")
            # Task will be rerouted by the IoT device
            return False
        
        # Call parent method if node is operational
        super().receive_task(task)
        return True


class EnhancedIoTDevice(IoTDevice):
    """
    Enhanced IoT Device with failure-aware routing and rerouting capabilities.
    """
    
    def __init__(self, device_id: str, location: Location,
                 computational_resources: ComputationalResources,
                 fog_node: 'EnhancedFogNode', env: simpy.Environment,
                 config_manager: ConfigManager):
        super().__init__(device_id, location, computational_resources, fog_node, env)
        self.config_manager = config_manager
        self.primary_fog_node = fog_node
        self.alternative_fog_nodes: List['EnhancedFogNode'] = []
        self.cloud_server = None  # Will be set during setup
        
        # Load configuration parameters
        task_config = config_manager.get_task_generation_config()
        self.task_generation_rate = random.uniform(*task_config.generation_rate_range)
        self.task_complexity_range = task_config.complexity_range
        self.deadline_range = task_config.deadline_range
        self.task_size_range = task_config.data_size_range
    
    def set_alternative_fog_nodes(self, alternative_nodes: List['EnhancedFogNode']):
        """Set alternative fog nodes for rerouting."""
        self.alternative_fog_nodes = alternative_nodes
    
    def set_cloud_server(self, cloud_server: 'CloudServer'):
        """Set the cloud server for direct routing."""
        self.cloud_server = cloud_server
    
    def find_operational_fog_node(self) -> Optional['EnhancedFogNode']:
        """
        Find an operational fog node for task routing.
        
        Returns:
            An operational fog node or None if none available
        """
        # Check primary fog node first
        if self.primary_fog_node.is_operational():
            return self.primary_fog_node
        
        # Check alternative fog nodes
        for fog_node in self.alternative_fog_nodes:
            if fog_node.is_operational():
                return fog_node
        
        return None
    
    def send_task_to_fog(self, task: Task) -> bool:
        """
        Enhanced task sending with failure-aware routing.
        
        Args:
            task: The task to be sent
            
        Returns:
            True if task was sent successfully, False otherwise
        """
        try:
            # Find operational fog node
            target_fog_node = self.find_operational_fog_node()
            
            if target_fog_node is None:
                # No operational fog nodes, send directly to cloud
                print(f"☁️ {self.device_id}: No operational fog nodes, routing to cloud")
                return self.send_task_to_cloud(task)
            
            # Calculate network latency
            distance = self.location.distance_to(target_fog_node.location)
            network_latency = distance * self.config_manager.get_network_latency_config().base_latency_per_distance
            
            # Simulate network transmission delay
            yield self.env.timeout(network_latency)
            
            # Update task with transmission information
            task.transmission_time = self.env.now
            task.network_latency = network_latency
            
            # Send task to fog node
            if target_fog_node.receive_task(task):
                self.tasks_sent += 1
                print(f"📤 {self.device_id}: Sent task {task.task_id} to {target_fog_node.node_id} (latency: {network_latency:.3f}s)")
                return True
            else:
                # Fog node failed to receive task, try cloud
                print(f"☁️ {self.device_id}: Fog node failed, routing to cloud")
                return self.send_task_to_cloud(task)
            
        except Exception as e:
            print(f"❌ {self.device_id}: Failed to send task {task.task_id}: {e}")
            self.tasks_failed += 1
            return False
    
    def send_task_to_cloud(self, task: Task) -> bool:
        """
        Send task directly to cloud server.
        
        Args:
            task: The task to be sent
            
        Returns:
            True if task was sent successfully, False otherwise
        """
        if not self.cloud_server:
            print(f"❌ {self.device_id}: No cloud server available")
            self.tasks_failed += 1
            return False
        
        try:
            # Calculate network latency to cloud
            distance = self.location.distance_to(self.cloud_server.location)
            network_latency = distance * self.config_manager.get_network_latency_config().base_latency_per_distance
            network_latency += self.config_manager.get_network_latency_config().cloud_latency_base
            
            # Simulate network transmission delay
            yield self.env.timeout(network_latency)
            
            # Update task with transmission information
            task.transmission_time = self.env.now
            task.network_latency = network_latency
            
            # Send task to cloud server
            self.cloud_server.receive_task(task)
            self.tasks_sent += 1
            
            print(f"📤 {self.device_id}: Sent task {task.task_id} to cloud (latency: {network_latency:.3f}s)")
            return True
            
        except Exception as e:
            print(f"❌ {self.device_id}: Failed to send task {task.task_id} to cloud: {e}")
            self.tasks_failed += 1
            return False


class EnhancedFogComputingSimulation(FogComputingSimulation):
    """
    Enhanced Fog Computing Simulation with configuration management and failure simulation.
    """
    
    def __init__(self, config_file: str = "config.json"):
        """
        Initialize enhanced simulation with configuration.
        
        Args:
            config_file: Path to configuration file
        """
        # Load configuration
        self.config_manager = ConfigManager(config_file)
        sim_config = self.config_manager.get_simulation_config()
        
        # Initialize base simulation
        super().__init__(simulation_time=sim_config.duration)
        
        # Set random seed
        random.seed(sim_config.random_seed)
        
        # Enhanced components
        self.enhanced_fog_nodes: List[EnhancedFogNode] = []
        self.enhanced_iot_devices: List[EnhancedIoTDevice] = []
        self.failure_events: List[NodeFailure] = []
        
        # Load configuration parameters
        self.sim_config = sim_config
        self.network_config = self.config_manager.get_network_topology_config()
        self.task_config = self.config_manager.get_task_generation_config()
        self.latency_config = self.config_manager.get_network_latency_config()
        self.perf_config = self.config_manager.get_performance_monitoring_config()
    
    def setup_simulation(self):
        """Enhanced simulation setup with configuration."""
        print("🔧 Setting up Enhanced Fog Computing Simulation")
        print("=" * 60)
        
        # Print configuration summary
        self.config_manager.print_config_summary()
        
        # Create cloud server
        self._create_cloud_server()
        
        # Create fog nodes
        self._create_fog_nodes()
        
        # Create IoT devices
        self._create_iot_devices()
        
        # Establish network topology
        self._establish_network_topology()
        
        # Initialize SimPy resources
        self.initialize_simpy_resources()
        
        # Start failure simulation if enabled
        if self.sim_config.enable_node_failures:
            self.env.process(self.failure_simulation_process())
        
        print("✅ Enhanced simulation environment setup complete!")
    
    def _create_cloud_server(self):
        """Create cloud server from configuration."""
        cloud_config = self.network_config.cloud_server_config
        location = Location(
            cloud_config['location']['x'],
            cloud_config['location']['y']
        )
        resources = ComputationalResources(
            cpu_mips=cloud_config['resources']['cpu_mips'],
            memory=cloud_config['resources']['memory_mb'],
            storage=cloud_config['resources']['storage_mb']
        )
        
        self.cloud_server = CloudServer(
            server_id="CLOUD_001",
            location=location,
            computational_resources=resources,
            env=self.env
        )
    
    def _create_fog_nodes(self):
        """Create fog nodes from configuration."""
        fog_config = self.network_config.fog_nodes_config
        locations = fog_config.get('locations', [])
        resources_range = fog_config.get('resources_range', {})
        
        for i in range(self.network_config.num_fog_nodes):
            # Get location
            if i < len(locations):
                location = Location(locations[i]['x'], locations[i]['y'])
            else:
                location = Location(
                    random.uniform(10, 90),
                    random.uniform(10, 90)
                )
            
            # Generate resources
            resources = ComputationalResources(
                cpu_mips=random.uniform(
                    resources_range['cpu_mips']['min'],
                    resources_range['cpu_mips']['max']
                ),
                memory=random.uniform(
                    resources_range['memory_mb']['min'],
                    resources_range['memory_mb']['max']
                ),
                storage=random.uniform(
                    resources_range['storage_mb']['min'],
                    resources_range['storage_mb']['max']
                )
            )
            
            # Create enhanced fog node
            fog_node = EnhancedFogNode(
                node_id=f"FOG_{i+1:03d}",
                location=location,
                computational_resources=resources,
                cloud_server=self.cloud_server,
                env=self.env,
                config_manager=self.config_manager
            )
            
            self.enhanced_fog_nodes.append(fog_node)
            self.fog_nodes.append(fog_node)  # Also add to base list
    
    def _create_iot_devices(self):
        """Create IoT devices from configuration."""
        iot_config = self.network_config.iot_devices_config
        resources_range = iot_config.get('resources_range', {})
        
        for i in range(self.network_config.num_iot_devices):
            # Generate location
            location = Location(
                random.uniform(5, 95),
                random.uniform(5, 95)
            )
            
            # Generate resources
            resources = ComputationalResources(
                cpu_mips=random.uniform(
                    resources_range['cpu_mips']['min'],
                    resources_range['cpu_mips']['max']
                ),
                memory=random.uniform(
                    resources_range['memory_mb']['min'],
                    resources_range['memory_mb']['max']
                ),
                storage=random.uniform(
                    resources_range['storage_mb']['min'],
                    resources_range['storage_mb']['max']
                )
            )
            
            # Create enhanced IoT device
            iot_device = EnhancedIoTDevice(
                device_id=f"IOT_{i+1:03d}",
                location=location,
                computational_resources=resources,
                fog_node=None,  # Will be set during topology establishment
                env=self.env,
                config_manager=self.config_manager
            )
            
            self.enhanced_iot_devices.append(iot_device)
            self.iot_devices.append(iot_device)  # Also add to base list
    
    def _establish_network_topology(self):
        """Establish network topology with failure-aware routing."""
        # Connect IoT devices to nearest fog nodes
        for iot_device in self.enhanced_iot_devices:
            # Find nearest fog node
            nearest_fog = min(self.enhanced_fog_nodes, 
                             key=lambda fog: iot_device.location.distance_to(fog.location))
            
            # Set primary fog node
            iot_device.primary_fog_node = nearest_fog
            nearest_fog.add_iot_device(iot_device)
            
            # Set alternative fog nodes (all other fog nodes)
            alternative_nodes = [fog for fog in self.enhanced_fog_nodes if fog != nearest_fog]
            iot_device.set_alternative_fog_nodes(alternative_nodes)
            
            # Set cloud server
            iot_device.set_cloud_server(self.cloud_server)
    
    def failure_simulation_process(self):
        """
        SimPy process that simulates random node failures.
        """
        while True:
            # Wait for random interval before next failure
            yield self.env.timeout(random.expovariate(self.sim_config.failure_probability))
            
            # Select a random fog node to fail
            operational_nodes = [node for node in self.enhanced_fog_nodes if node.is_operational()]
            if operational_nodes:
                failed_node = random.choice(operational_nodes)
                
                # Generate failure duration
                failure_duration = random.uniform(*self.sim_config.failure_duration_range)
                
                # Simulate failure
                failed_node.simulate_failure(self.env.now, failure_duration)
                self.failure_events.append(failed_node.current_failure)
                
                # Schedule recovery
                self.env.process(self.recovery_process(failed_node, failure_duration))
    
    def recovery_process(self, failed_node: EnhancedFogNode, failure_duration: float):
        """
        SimPy process that handles node recovery.
        
        Args:
            failed_node: The node that failed
            failure_duration: How long the failure lasts
        """
        # Wait for failure duration
        yield self.env.timeout(failure_duration)
        
        # Recover the node
        failed_node.recover_from_failure(self.env.now)
    
    def print_enhanced_simulation_results(self):
        """Print enhanced simulation results with failure statistics."""
        # Call base results
        super().print_simulation_results()
        
        # Add failure statistics
        print(f"\n💥 Node Failure Statistics:")
        total_failures = len(self.failure_events)
        print(f"   Total failures: {total_failures}")
        
        if total_failures > 0:
            # Calculate failure statistics
            failure_durations = [f.failure_duration for f in self.failure_events]
            avg_failure_duration = sum(failure_durations) / len(failure_durations)
            max_failure_duration = max(failure_durations)
            
            print(f"   Average failure duration: {avg_failure_duration:.2f}s")
            print(f"   Maximum failure duration: {max_failure_duration:.2f}s")
            
            # Show failure timeline
            print(f"\n   Failure Timeline:")
            for failure in self.failure_events:
                print(f"      {failure.node_id}: {failure.failure_time:.2f}s - {failure.recovery_time:.2f}s ({failure.failure_duration:.2f}s)")
        
        # Show operational status
        print(f"\n🔧 Current Node Status:")
        for fog_node in self.enhanced_fog_nodes:
            status_icon = "✅" if fog_node.is_operational() else "❌"
            print(f"   {status_icon} {fog_node.node_id}: {fog_node.status.value}")


def run_enhanced_simulation(config_file: str = "config.json"):
    """
    Run enhanced fog computing simulation with configuration and failure simulation.
    
    Args:
        config_file: Path to configuration file
        
    Returns:
        EnhancedFogComputingSimulation: The completed simulation object
    """
    print("🌐 Enhanced Fog Computing Simulation with Advanced Features")
    print("=" * 70)
    
    # Create and setup simulation
    simulation = EnhancedFogComputingSimulation(config_file)
    simulation.setup_simulation()
    
    # Run simulation
    simulation.run_simulation()
    
    # Print enhanced results
    simulation.print_enhanced_simulation_results()
    
    return simulation


if __name__ == "__main__":
    # Run enhanced simulation
    simulation = run_enhanced_simulation()
