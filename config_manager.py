"""
Configuration Manager
====================

This module handles loading and managing simulation configuration from config.json.
Provides a centralized way to configure all simulation parameters.
"""

import json
import os
from typing import Dict, Any, List, Tuple
from dataclasses import dataclass


@dataclass
class SimulationConfig:
    """Configuration class for simulation parameters."""
    duration: float
    random_seed: int
    enable_node_failures: bool
    failure_probability: float
    failure_duration_range: Tuple[float, float]


@dataclass
class NetworkTopologyConfig:
    """Configuration class for network topology."""
    num_fog_nodes: int
    num_iot_devices: int
    cloud_server_config: Dict[str, Any]
    fog_nodes_config: Dict[str, Any]
    iot_devices_config: Dict[str, Any]


@dataclass
class TaskGenerationConfig:
    """Configuration class for task generation parameters."""
    generation_rate_range: Tuple[float, float]
    complexity_range: Tuple[float, float]
    deadline_range: Tuple[float, float]
    data_size_range: Tuple[float, float]


@dataclass
class NetworkLatencyConfig:
    """Configuration class for network latency parameters."""
    base_latency_per_distance: float
    cloud_latency_base: float
    fog_to_cloud_multiplier: float


@dataclass
class OffloadingConfig:
    """Configuration class for offloading decision parameters."""
    complexity_threshold: float
    utilization_threshold: float
    deadline_threshold: float
    queue_length_threshold: int


@dataclass
class PerformanceMonitoringConfig:
    """Configuration class for performance monitoring parameters."""
    monitoring_interval: float
    enable_detailed_logging: bool
    export_data: bool


class ConfigManager:
    """
    Manages simulation configuration loading and access.
    """
    
    def __init__(self, config_file: str = "config.json"):
        """
        Initialize the configuration manager.
        
        Args:
            config_file: Path to the configuration file
        """
        self.config_file = config_file
        self.config_data = {}
        self.simulation_config = None
        self.network_topology_config = None
        self.task_generation_config = None
        self.network_latency_config = None
        self.offloading_config = None
        self.performance_monitoring_config = None
        
        self.load_config()
    
    def load_config(self):
        """Load configuration from JSON file."""
        try:
            if not os.path.exists(self.config_file):
                raise FileNotFoundError(f"Configuration file {self.config_file} not found")
            
            with open(self.config_file, 'r') as f:
                self.config_data = json.load(f)
            
            # Parse configuration sections
            self._parse_simulation_config()
            self._parse_network_topology_config()
            self._parse_task_generation_config()
            self._parse_network_latency_config()
            self._parse_offloading_config()
            self._parse_performance_monitoring_config()
            
            print(f"✅ Configuration loaded successfully from {self.config_file}")
            
        except Exception as e:
            print(f"❌ Error loading configuration: {e}")
            raise e
    
    def _parse_simulation_config(self):
        """Parse simulation configuration section."""
        sim_config = self.config_data.get('simulation', {})
        self.simulation_config = SimulationConfig(
            duration=sim_config.get('duration', 100.0),
            random_seed=sim_config.get('random_seed', 42),
            enable_node_failures=sim_config.get('enable_node_failures', True),
            failure_probability=sim_config.get('failure_probability', 0.1),
            failure_duration_range=tuple(sim_config.get('failure_duration_range', [5.0, 15.0]))
        )
    
    def _parse_network_topology_config(self):
        """Parse network topology configuration section."""
        network_config = self.config_data.get('network_topology', {})
        self.network_topology_config = NetworkTopologyConfig(
            num_fog_nodes=network_config.get('num_fog_nodes', 3),
            num_iot_devices=network_config.get('num_iot_devices', 10),
            cloud_server_config=network_config.get('cloud_server', {}),
            fog_nodes_config=network_config.get('fog_nodes', {}),
            iot_devices_config=network_config.get('iot_devices', {})
        )
    
    def _parse_task_generation_config(self):
        """Parse task generation configuration section."""
        task_config = self.config_data.get('task_generation', {})
        self.task_generation_config = TaskGenerationConfig(
            generation_rate_range=tuple(task_config.get('generation_rate_range', [0.1, 0.3])),
            complexity_range=tuple(task_config.get('complexity_range', [50, 2000])),
            deadline_range=tuple(task_config.get('deadline_range', [5, 30])),
            data_size_range=tuple(task_config.get('data_size_range', [100, 1000]))
        )
    
    def _parse_network_latency_config(self):
        """Parse network latency configuration section."""
        latency_config = self.config_data.get('network_latency', {})
        self.network_latency_config = NetworkLatencyConfig(
            base_latency_per_distance=latency_config.get('base_latency_per_distance', 0.01),
            cloud_latency_base=latency_config.get('cloud_latency_base', 5.0),
            fog_to_cloud_multiplier=latency_config.get('fog_to_cloud_multiplier', 0.02)
        )
    
    def _parse_offloading_config(self):
        """Parse offloading configuration section."""
        offload_config = self.config_data.get('offloading_parameters', {})
        self.offloading_config = OffloadingConfig(
            complexity_threshold=offload_config.get('complexity_threshold', 1000.0),
            utilization_threshold=offload_config.get('utilization_threshold', 0.8),
            deadline_threshold=offload_config.get('deadline_threshold', 5.0),
            queue_length_threshold=offload_config.get('queue_length_threshold', 5)
        )
    
    def _parse_performance_monitoring_config(self):
        """Parse performance monitoring configuration section."""
        perf_config = self.config_data.get('performance_monitoring', {})
        self.performance_monitoring_config = PerformanceMonitoringConfig(
            monitoring_interval=perf_config.get('monitoring_interval', 1.0),
            enable_detailed_logging=perf_config.get('enable_detailed_logging', True),
            export_data=perf_config.get('export_data', True)
        )
    
    def get_simulation_config(self) -> SimulationConfig:
        """Get simulation configuration."""
        return self.simulation_config
    
    def get_network_topology_config(self) -> NetworkTopologyConfig:
        """Get network topology configuration."""
        return self.network_topology_config
    
    def get_task_generation_config(self) -> TaskGenerationConfig:
        """Get task generation configuration."""
        return self.task_generation_config
    
    def get_network_latency_config(self) -> NetworkLatencyConfig:
        """Get network latency configuration."""
        return self.network_latency_config
    
    def get_offloading_config(self) -> OffloadingConfig:
        """Get offloading configuration."""
        return self.offloading_config
    
    def get_performance_monitoring_config(self) -> PerformanceMonitoringConfig:
        """Get performance monitoring configuration."""
        return self.performance_monitoring_config
    
    def print_config_summary(self):
        """Print a summary of the loaded configuration."""
        print("\n📋 Configuration Summary")
        print("=" * 40)
        
        if self.simulation_config:
            print(f"Simulation Duration: {self.simulation_config.duration}s")
            print(f"Random Seed: {self.simulation_config.random_seed}")
            print(f"Node Failures Enabled: {self.simulation_config.enable_node_failures}")
            if self.simulation_config.enable_node_failures:
                print(f"Failure Probability: {self.simulation_config.failure_probability}")
        
        if self.network_topology_config:
            print(f"Fog Nodes: {self.network_topology_config.num_fog_nodes}")
            print(f"IoT Devices: {self.network_topology_config.num_iot_devices}")
        
        if self.offloading_config:
            print(f"Complexity Threshold: {self.offloading_config.complexity_threshold}")
            print(f"Utilization Threshold: {self.offloading_config.utilization_threshold}")
        
        print("✅ Configuration summary complete!")


def create_default_config():
    """Create a default configuration file if it doesn't exist."""
    default_config = {
        "simulation": {
            "duration": 100.0,
            "random_seed": 42,
            "enable_node_failures": True,
            "failure_probability": 0.1,
            "failure_duration_range": [5.0, 15.0]
        },
        "network_topology": {
            "num_fog_nodes": 3,
            "num_iot_devices": 10,
            "cloud_server": {
                "location": {"x": 50, "y": 50},
                "resources": {
                    "cpu_mips": 10000,
                    "memory_mb": 32000,
                    "storage_mb": 1000000
                }
            },
            "fog_nodes": {
                "locations": [
                    {"x": 20, "y": 20},
                    {"x": 80, "y": 20},
                    {"x": 50, "y": 80}
                ],
                "resources_range": {
                    "cpu_mips": {"min": 1000, "max": 3000},
                    "memory_mb": {"min": 4000, "max": 8000},
                    "storage_mb": {"min": 100000, "max": 500000}
                }
            },
            "iot_devices": {
                "resources_range": {
                    "cpu_mips": {"min": 50, "max": 200},
                    "memory_mb": {"min": 256, "max": 1024},
                    "storage_mb": {"min": 1000, "max": 10000}
                }
            }
        },
        "task_generation": {
            "generation_rate_range": [0.1, 0.3],
            "complexity_range": [50, 2000],
            "deadline_range": [5, 30],
            "data_size_range": [100, 1000]
        },
        "network_latency": {
            "base_latency_per_distance": 0.01,
            "cloud_latency_base": 5.0,
            "fog_to_cloud_multiplier": 0.02
        },
        "offloading_parameters": {
            "complexity_threshold": 1000.0,
            "utilization_threshold": 0.8,
            "deadline_threshold": 5.0,
            "queue_length_threshold": 5
        },
        "performance_monitoring": {
            "monitoring_interval": 1.0,
            "enable_detailed_logging": True,
            "export_data": True
        }
    }
    
    with open("config.json", 'w') as f:
        json.dump(default_config, f, indent=2)
    
    print("✅ Default configuration file created: config.json")


if __name__ == "__main__":
    # Test configuration manager
    try:
        config_manager = ConfigManager()
        config_manager.print_config_summary()
    except FileNotFoundError:
        print("Creating default configuration file...")
        create_default_config()
        config_manager = ConfigManager()
        config_manager.print_config_summary()
