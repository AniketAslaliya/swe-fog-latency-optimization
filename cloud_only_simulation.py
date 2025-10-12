"""
Cloud-Only Simulation Mode
==========================

This module implements a cloud-only architecture simulation where IoT devices
send tasks directly to the cloud server, bypassing fog nodes completely.
This allows for comparative analysis against the fog architecture.
"""

import simpy
import random
import math
import time
from typing import List, Optional, Tuple, Dict, Any
from dataclasses import dataclass
from enum import Enum

# Import the base classes from fog_simulation
from fog_simulation import (
    Location, ComputationalResources, Task, TaskStatus, DeviceType,
    PerformanceLogger, global_logger
)


class CloudOnlySimulation:
    """
    Cloud-only simulation environment where IoT devices send tasks
    directly to the cloud server, bypassing fog nodes.
    """
    
    def __init__(self, simulation_time: float = 100.0):
        """
        Initialize the cloud-only simulation.
        
        Args:
            simulation_time: Duration of the simulation in seconds
        """
        self.simulation_time = simulation_time
        self.env = simpy.Environment()
        self.cloud_server = None
        self.iot_devices: List['CloudOnlyIoTDevice'] = []
        self.start_time = 0.0
        self.end_time = 0.0
        
        # Performance logger for this simulation
        self.performance_logger = PerformanceLogger()
    
    def setup_simulation(self, num_iot_devices: int = 10):
        """
        Set up the cloud-only simulation environment.
        
        Args:
            num_iot_devices: Number of IoT devices to create
        """
        print("🔧 Setting up Cloud-Only Simulation Environment")
        print("=" * 60)
        
        # Create cloud server (same as fog simulation)
        self.cloud_server = CloudOnlyCloudServer(
            server_id="CLOUD_ONLY_001",
            location=Location(50, 50),
            computational_resources=ComputationalResources(
                cpu_mips=10000,  # 10,000 MIPS
                memory=32000,    # 32 GB
                storage=1000000   # 1 TB
            ),
            env=self.env
        )
        
        # Create IoT devices that connect directly to cloud
        for i in range(num_iot_devices):
            iot_device = CloudOnlyIoTDevice(
                device_id=f"CLOUD_IOT_{i+1:03d}",
                location=Location(
                    random.uniform(5, 95), random.uniform(5, 95)
                ),
                computational_resources=ComputationalResources(
                    cpu_mips=random.uniform(50, 200),   # 50-200 MIPS
                    memory=random.uniform(256, 1024),  # 256 MB - 1 GB
                    storage=random.uniform(1000, 10000)  # 1-10 GB
                ),
                cloud_server=self.cloud_server,
                env=self.env,
                performance_logger=self.performance_logger
            )
            self.iot_devices.append(iot_device)
        
        # Initialize SimPy resources
        self.initialize_simpy_resources()
        
        print(f"\n📊 Cloud-Only Network Summary:")
        print(f"   Cloud Server: {self.cloud_server.server_id}")
        print(f"   IoT Devices: {len(self.iot_devices)}")
        print(f"   Cloud Processing Capacity: {self.cloud_server.processing_capacity.capacity}")
        print(f"✅ Cloud-only simulation environment setup complete!")
    
    def initialize_simpy_resources(self):
        """Initialize SimPy resources for processing capacity modeling."""
        # Cloud server processing capacity (higher than fog nodes)
        self.cloud_server.processing_capacity = simpy.Resource(
            self.env, 
            capacity=self.cloud_server.computational_resources.cpu_mips // 1000
        )
    
    def start_task_generation(self):
        """Start task generation processes for all IoT devices."""
        print("\n🔄 Starting Cloud-Only Task Generation...")
        for iot_device in self.iot_devices:
            self.env.process(iot_device.task_generation_process())
            print(f"   ✓ Started task generation for {iot_device.device_id}")
    
    def resource_monitoring_process(self):
        """
        SimPy process that periodically monitors and logs resource utilization.
        """
        while True:
            # Monitor cloud server
            cloud_utilization = self.cloud_server.get_utilization()
            cloud_queue_length = len(self.cloud_server.pending_tasks)
            cloud_capacity = self.cloud_server.processing_capacity.capacity if self.cloud_server.processing_capacity else 0
            
            self.performance_logger.log_resource_utilization(
                timestamp=self.env.now,
                node_id=self.cloud_server.server_id,
                utilization=cloud_utilization,
                queue_length=cloud_queue_length,
                processing_capacity=cloud_capacity,
                node_type='cloud_only'
            )
            
            # Wait before next monitoring cycle
            yield self.env.timeout(1.0)  # Monitor every 1 simulation time unit
    
    def run_simulation(self):
        """Run the cloud-only simulation for the specified duration."""
        print(f"\n🚀 Starting Cloud-Only Simulation for {self.simulation_time} seconds...")
        print("=" * 50)
        
        # Start task generation
        self.start_task_generation()
        
        # Start resource monitoring process
        print("\n📊 Starting Resource Monitoring...")
        self.env.process(self.resource_monitoring_process())
        print("   ✓ Started resource utilization monitoring")
        
        self.start_time = self.env.now
        self.env.run(until=self.simulation_time)
        self.end_time = self.env.now
        
        print(f"✅ Cloud-only simulation completed in {self.end_time - self.start_time:.2f} seconds")
    
    def print_simulation_results(self):
        """Print comprehensive cloud-only simulation results."""
        print("\n📊 Cloud-Only Simulation Results")
        print("=" * 50)
        
        # IoT device statistics
        total_tasks_generated = sum(device.tasks_generated for device in self.iot_devices)
        total_tasks_sent = sum(device.tasks_sent for device in self.iot_devices)
        total_tasks_failed = sum(device.tasks_failed for device in self.iot_devices)
        
        print(f"\n📱 IoT Device Statistics:")
        print(f"   Total tasks generated: {total_tasks_generated}")
        print(f"   Total tasks sent: {total_tasks_sent}")
        print(f"   Total tasks failed: {total_tasks_failed}")
        print(f"   Success rate: {(total_tasks_sent / total_tasks_generated * 100):.1f}%" if total_tasks_generated > 0 else "   Success rate: 0%")
        
        # Cloud server statistics
        print(f"\n☁️  Cloud Server Statistics:")
        cloud_stats = self.cloud_server.get_task_statistics()
        print(f"   Cloud Server ({self.cloud_server.server_id}):")
        print(f"      Tasks processed: {cloud_stats['tasks_processed']}")
        print(f"      Tasks failed: {cloud_stats['tasks_failed']}")
        print(f"      Average processing time: {cloud_stats['average_processing_time']:.3f}s")
        print(f"      Resource utilization: {cloud_stats['utilization']:.1%}")
        print(f"      Pending tasks: {cloud_stats['pending_tasks']}")
        
        # Performance monitoring summary
        print(f"\n📈 Performance Monitoring Summary:")
        performance_summary = self.performance_logger.get_performance_summary()
        if performance_summary:
            print(f"   Total events logged: {performance_summary.get('total_events', 0)}")
            print(f"   Total tasks tracked: {performance_summary.get('total_tasks', 0)}")
            print(f"   Average response time: {performance_summary.get('average_response_time', 0):.3f}s")
            print(f"   Average processing time: {performance_summary.get('average_processing_time', 0):.3f}s")
            print(f"   Resource monitoring entries: {performance_summary.get('resource_monitoring_entries', 0)}")
        
        print(f"\n⏱️  Simulation Duration: {self.end_time - self.start_time:.2f} seconds")
        print(f"\n🎉 Cloud-only simulation completed successfully!")
        print("✅ Direct cloud processing architecture implemented!")


class CloudOnlyIoTDevice:
    """
    IoT Device for cloud-only simulation that sends tasks directly to cloud.
    """
    
    def __init__(self, device_id: str, location: Location, 
                 computational_resources: ComputationalResources,
                 cloud_server: 'CloudOnlyCloudServer', env: simpy.Environment,
                 performance_logger: PerformanceLogger):
        self.device_id = device_id
        self.location = location
        self.computational_resources = computational_resources
        self.connected_cloud_server = cloud_server
        self.env = env
        self.performance_logger = performance_logger
        
        # Task generation parameters
        self.task_generation_rate = random.uniform(0.1, 0.3)  # Tasks per second
        self.task_complexity_range = (50, 2000)  # MIPS range
        self.deadline_range = (5, 30)  # Time units
        self.task_size_range = (100, 1000)  # Data size in MB
        
        # Statistics
        self.tasks_generated = 0
        self.tasks_sent = 0
        self.tasks_failed = 0
    
    def generate_task(self) -> Task:
        """Generate a new computational task."""
        self.tasks_generated += 1
        
        # Generate task parameters
        complexity = random.uniform(*self.task_complexity_range)
        deadline = self.env.now + random.uniform(*self.deadline_range)
        data_size = random.uniform(*self.task_size_range)
        
        # Create task
        task = Task(
            task_id=f"{self.device_id}_TASK_{self.tasks_generated:03d}",
            creation_time=self.env.now,
            complexity_mips=complexity,
            deadline=deadline,
            source_device_id=self.device_id,
            data_size=data_size
        )
        
        # Log task creation event
        self.performance_logger.log_task_event(
            event_type='creation_time',
            task_id=task.task_id,
            timestamp=self.env.now,
            task_complexity=complexity,
            processing_location=self.device_id
        )
        
        return task
    
    def send_task_to_cloud(self, task: Task) -> bool:
        """
        Send a task directly to the cloud server with network latency simulation.
        
        Args:
            task: The task to be sent
            
        Returns:
            True if task was sent successfully, False otherwise
        """
        try:
            # Calculate network latency to cloud
            distance = self.location.distance_to(self.connected_cloud_server.location)
            network_latency = distance * 0.01  # Base latency per distance unit
            
            # Simulate network transmission delay
            yield self.env.timeout(network_latency)
            
            # Update task with transmission information
            task.transmission_time = self.env.now
            task.network_latency = network_latency
            
            # Send task to cloud server
            self.connected_cloud_server.receive_task(task)
            self.tasks_sent += 1
            
            print(f"📤 {self.device_id}: Sent task {task.task_id} to cloud (latency: {network_latency:.3f}s)")
            return True
            
        except Exception as e:
            print(f"❌ {self.device_id}: Failed to send task {task.task_id}: {e}")
            self.tasks_failed += 1
            return False
    
    def task_generation_process(self):
        """
        SimPy process that continuously generates tasks.
        """
        while True:
            # Generate a new task
            task = self.generate_task()
            
            # Send task to cloud
            yield from self.send_task_to_cloud(task)
            
            # Wait before generating next task
            yield self.env.timeout(random.expovariate(self.task_generation_rate))


class CloudOnlyCloudServer:
    """
    Cloud Server for cloud-only simulation.
    """
    
    def __init__(self, server_id: str, location: Location, 
                 computational_resources: ComputationalResources, env: simpy.Environment):
        self.server_id = server_id
        self.location = location
        self.computational_resources = computational_resources
        self.env = env
        self.processing_capacity = None
        
        # Statistics
        self.tasks_processed = 0
        self.tasks_failed = 0
        self.total_processing_time = 0.0
        self.pending_tasks: List[Task] = []
    
    def receive_task(self, task: Task):
        """
        Receive a task from an IoT device and add it to the processing queue.
        
        Args:
            task: The task to be processed
        """
        print(f"📥 {self.server_id}: Received task {task.task_id} from {task.source_device_id}")
        self.pending_tasks.append(task)
        
        # Log task arrival at cloud server
        global_logger.log_task_event(
            event_type='arrival_at_cloud_time',
            task_id=task.task_id,
            timestamp=self.env.now,
            task_complexity=task.complexity_mips,
            processing_location=self.server_id
        )
        
        # Start processing the task
        if self.env:
            self.env.process(self.handle_task(task))
    
    def handle_task(self, task: Task):
        """
        Handle a task by processing it on the cloud server.
        This is a SimPy process that manages task execution.
        
        Args:
            task: The task to be processed
        """
        try:
            # Check if task is overdue
            if task.is_overdue(self.env.now):
                print(f"⏰ {self.server_id}: Task {task.task_id} is overdue, marking as timeout")
                task.status = TaskStatus.TIMEOUT
                self.tasks_failed += 1
                return
            
            # Request CPU resource
            print(f"🔄 {self.server_id}: Starting cloud processing of task {task.task_id}")
            task.status = TaskStatus.PROCESSING
            task.start_time = self.env.now
            task.processing_node = self.server_id
            
            # Log processing start time
            task.processing_start_time = self.env.now
            global_logger.log_task_event(
                event_type='processing_start_time',
                task_id=task.task_id,
                timestamp=self.env.now,
                task_complexity=task.complexity_mips,
                processing_location=self.server_id
            )
            
            with self.processing_capacity.request() as cpu_request:
                # Wait for CPU resource
                yield cpu_request
                
                # Calculate processing time
                processing_time = task.get_processing_time(self.computational_resources.cpu_mips)
                
                # Simulate processing delay
                yield self.env.timeout(processing_time)
                
                # Task completed
                task.status = TaskStatus.COMPLETED
                task.completion_time = self.env.now
                
                # Log processing end time
                task.processing_end_time = self.env.now
                global_logger.log_task_event(
                    event_type='processing_end_time',
                    task_id=task.task_id,
                    timestamp=self.env.now,
                    task_complexity=task.complexity_mips,
                    processing_location=self.server_id,
                    additional_data={'processing_time': processing_time}
                )
                
                # Update statistics
                self.tasks_processed += 1
                self.total_processing_time += processing_time
                
                print(f"✅ {self.server_id}: Completed task {task.task_id} "
                      f"(processing time: {processing_time:.3f}s, "
                      f"total time: {task.get_response_time():.3f}s)")
                
        except Exception as e:
            print(f"❌ {self.server_id}: Error processing task {task.task_id}: {e}")
            task.status = TaskStatus.FAILED
            self.tasks_failed += 1
    
    def get_utilization(self) -> float:
        """Calculate current CPU utilization."""
        if not self.processing_capacity:
            return 0.0
        
        in_use = self.processing_capacity.count
        capacity = self.processing_capacity.capacity
        return in_use / capacity if capacity > 0 else 0.0
    
    def get_task_statistics(self) -> dict:
        """Get comprehensive task processing statistics."""
        return {
            'tasks_processed': self.tasks_processed,
            'tasks_failed': self.tasks_failed,
            'average_processing_time': self.total_processing_time / self.tasks_processed if self.tasks_processed > 0 else 0,
            'utilization': self.get_utilization(),
            'pending_tasks': len(self.pending_tasks)
        }


def run_cloud_only_simulation(simulation_time: float = 100.0, num_iot_devices: int = 10):
    """
    Run a complete cloud-only simulation.
    
    Args:
        simulation_time: Duration of the simulation
        num_iot_devices: Number of IoT devices
        
    Returns:
        CloudOnlySimulation: The completed simulation object
    """
    print("🌐 Cloud-Only Architecture Simulation")
    print("=" * 50)
    
    # Create and setup simulation
    simulation = CloudOnlySimulation(simulation_time=simulation_time)
    simulation.setup_simulation(num_iot_devices=num_iot_devices)
    
    # Run simulation
    simulation.run_simulation()
    
    # Print results
    simulation.print_simulation_results()
    
    return simulation


if __name__ == "__main__":
    # Run cloud-only simulation
    simulation = run_cloud_only_simulation(simulation_time=50.0, num_iot_devices=8)
