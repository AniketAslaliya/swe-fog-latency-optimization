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
import time
from typing import List, Optional, Tuple, Dict, Any
from dataclasses import dataclass
from enum import Enum


class DeviceType(Enum):
    """Enumeration for different types of network devices."""
    IOT_DEVICE = "iot_device"
    FOG_NODE = "fog_node"
    CLOUD_SERVER = "cloud_server"


class TaskStatus(Enum):
    """Enumeration for task processing status."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"


class OffloadDecision(Enum):
    """Enumeration for task offloading decisions."""
    PROCESS_LOCALLY = "process_locally"
    OFFLOAD_TO_CLOUD = "offload_to_cloud"


# Global performance monitoring and logging system
class PerformanceLogger:
    """Global performance monitoring and data logging system."""
    
    def __init__(self):
        self.task_events: List[Dict[str, Any]] = []
        self.resource_monitoring: List[Dict[str, Any]] = []
        self.simulation_metrics: Dict[str, Any] = {}
    
    def log_task_event(self, event_type: str, task_id: str, timestamp: float, 
                      task_complexity: float = None, decision_made: str = None, 
                      processing_location: str = None, additional_data: Dict[str, Any] = None):
        """
        Log a task event with detailed information.
        
        Args:
            event_type: Type of event (creation, arrival, decision, etc.)
            task_id: Unique task identifier
            timestamp: Simulation time when event occurred
            task_complexity: Task complexity in MIPS
            decision_made: Offloading decision made
            processing_location: Where task is being processed
            additional_data: Any additional event-specific data
        """
        event = {
            'event_type': event_type,
            'task_id': task_id,
            'timestamp': timestamp,
            'task_complexity': task_complexity,
            'decision_made': decision_made,
            'processing_location': processing_location,
            'additional_data': additional_data or {}
        }
        self.task_events.append(event)
    
    def log_resource_utilization(self, timestamp: float, node_id: str, 
                               utilization: float, queue_length: int, 
                               processing_capacity: int, node_type: str):
        """
        Log resource utilization for a node.
        
        Args:
            timestamp: Simulation time
            node_id: Node identifier
            utilization: CPU utilization percentage
            queue_length: Number of pending tasks
            processing_capacity: Total processing capacity
            node_type: Type of node (fog, cloud)
        """
        resource_log = {
            'timestamp': timestamp,
            'node_id': node_id,
            'utilization': utilization,
            'queue_length': queue_length,
            'processing_capacity': processing_capacity,
            'node_type': node_type
        }
        self.resource_monitoring.append(resource_log)
    
    def get_task_lifecycle(self, task_id: str) -> List[Dict[str, Any]]:
        """Get complete lifecycle events for a specific task."""
        return [event for event in self.task_events if event['task_id'] == task_id]
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get comprehensive performance summary."""
        if not self.task_events:
            return {}
        
        # Calculate task lifecycle metrics
        task_lifecycles = {}
        for event in self.task_events:
            task_id = event['task_id']
            if task_id not in task_lifecycles:
                task_lifecycles[task_id] = {}
            task_lifecycles[task_id][event['event_type']] = event['timestamp']
        
        # Calculate performance metrics
        response_times = []
        processing_times = []
        decision_times = []
        
        for task_id, lifecycle in task_lifecycles.items():
            if 'creation_time' in lifecycle and 'response_delivery_time' in lifecycle:
                response_time = lifecycle['response_delivery_time'] - lifecycle['creation_time']
                response_times.append(response_time)
            
            if 'processing_start_time' in lifecycle and 'processing_end_time' in lifecycle:
                processing_time = lifecycle['processing_end_time'] - lifecycle['processing_start_time']
                processing_times.append(processing_time)
            
            if 'creation_time' in lifecycle and 'decision_time' in lifecycle:
                decision_time = lifecycle['decision_time'] - lifecycle['creation_time']
                decision_times.append(decision_time)
        
        return {
            'total_events': len(self.task_events),
            'total_tasks': len(task_lifecycles),
            'average_response_time': sum(response_times) / len(response_times) if response_times else 0,
            'average_processing_time': sum(processing_times) / len(processing_times) if processing_times else 0,
            'average_decision_time': sum(decision_times) / len(decision_times) if decision_times else 0,
            'resource_monitoring_entries': len(self.resource_monitoring)
        }
    
    def export_data(self) -> Dict[str, Any]:
        """Export all logged data for analysis."""
        return {
            'task_events': self.task_events,
            'resource_monitoring': self.resource_monitoring,
            'performance_summary': self.get_performance_summary()
        }


# Global logger instance
global_logger = PerformanceLogger()


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


class Task:
    """
    Represents a computational task in the fog computing network.
    
    Tasks are generated by IoT devices and processed by fog nodes or cloud servers.
    Each task has specific computational requirements and deadlines.
    """
    
    def __init__(self, task_id: str, creation_time: float, complexity_mips: float, 
                 deadline: float, source_device_id: str, data_size: float = 0.0):
        """
        Initialize a computational task.
        
        Args:
            task_id: Unique identifier for the task
            creation_time: Simulation time when task was created
            complexity_mips: Computational complexity in MIPS
            deadline: Task deadline in simulation time units
            source_device_id: ID of the IoT device that generated the task
            data_size: Size of data associated with the task in MB
        """
        self.task_id = task_id
        self.creation_time = creation_time
        self.complexity_mips = complexity_mips
        self.deadline = deadline
        self.source_device_id = source_device_id
        self.data_size = data_size
        
        # Task status and processing information
        self.status = TaskStatus.PENDING
        self.start_time: Optional[float] = None
        self.completion_time: Optional[float] = None
        self.processing_node: Optional[str] = None
        
        # Network transmission information
        self.transmission_time: Optional[float] = None
        self.network_latency: float = 0.0
        
        # Offloading information
        self.offload_decision: Optional[OffloadDecision] = None
        self.offload_reason: Optional[str] = None
        self.cloud_transmission_time: Optional[float] = None
        self.cloud_network_latency: float = 0.0
        
        # Performance monitoring timestamps
        self.arrival_at_fog_time: Optional[float] = None
        self.decision_time: Optional[float] = None
        self.processing_start_time: Optional[float] = None
        self.processing_end_time: Optional[float] = None
        self.response_delivery_time: Optional[float] = None
        
    def __str__(self):
        return (f"Task {self.task_id} from {self.source_device_id} "
                f"(Complexity: {self.complexity_mips:.1f} MIPS, "
                f"Deadline: {self.deadline:.1f}, Status: {self.status.value})")
    
    def get_processing_time(self, node_cpu_mips: float) -> float:
        """
        Calculate the processing time for this task on a given node.
        
        Args:
            node_cpu_mips: CPU capacity of the processing node in MIPS
            
        Returns:
            Processing time in simulation time units
        """
        if node_cpu_mips <= 0:
            return float('inf')
        return self.complexity_mips / node_cpu_mips
    
    def is_overdue(self, current_time: float) -> bool:
        """Check if the task has exceeded its deadline."""
        return current_time > self.deadline
    
    def get_response_time(self) -> float:
        """Calculate total response time from creation to completion."""
        if self.completion_time is None:
            return 0.0
        return self.completion_time - self.creation_time
    
    def get_processing_delay(self) -> float:
        """Calculate processing delay (excluding network latency)."""
        if self.start_time is None or self.completion_time is None:
            return 0.0
        return self.completion_time - self.start_time


class IoTDevice:
    """
    Represents an IoT device in the fog computing network.
    
    IoT devices generate tasks and are connected to fog nodes for processing.
    They have limited computational resources and rely on fog/cloud for heavy processing.
    """
    
    def __init__(self, device_id: str, location: Location, 
                 computational_resources: ComputationalResources,
                 fog_node: Optional['FogNode'] = None, env: Optional[simpy.Environment] = None):
        """
        Initialize an IoT device.
        
        Args:
            device_id: Unique identifier for the device
            location: Physical location of the device
            computational_resources: Available computational resources
            fog_node: Connected fog node for task processing
            env: SimPy environment for task generation
        """
        self.device_id = device_id
        self.location = location
        self.computational_resources = computational_resources
        self.connected_fog_node = fog_node
        self.device_type = DeviceType.IOT_DEVICE
        self.env = env
        
        # Task generation parameters
        self.task_generation_rate = random.uniform(0.1, 0.5)  # Tasks per second
        self.task_size_range = (1, 10)  # MB
        self.task_complexity_range = (50, 500)  # MIPS
        self.deadline_range = (10, 50)  # Simulation time units
        
        # Task generation statistics
        self.tasks_generated = 0
        self.tasks_sent = 0
        self.tasks_failed = 0
        
    def __str__(self):
        return f"IoT Device {self.device_id} at {self.location} -> Fog Node {self.connected_fog_node.node_id if self.connected_fog_node else 'None'}"
    
    def get_nearest_fog_node(self, fog_nodes: List['FogNode']) -> 'FogNode':
        """Find the nearest fog node to this IoT device."""
        if not fog_nodes:
            raise ValueError("No fog nodes available")
        
        nearest_fog = min(fog_nodes, key=lambda fog: self.location.distance_to(fog.location))
        return nearest_fog
    
    def generate_task(self) -> Task:
        """
        Generate a new computational task.
        
        Returns:
            A new Task object with random parameters
        """
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
        global_logger.log_task_event(
            event_type='creation_time',
            task_id=task.task_id,
            timestamp=self.env.now,
            task_complexity=complexity,
            processing_location=self.device_id
        )
        
        return task
    
    def send_task_to_fog(self, task: Task) -> bool:
        """
        Send a task to the connected fog node with network latency simulation.
        
        Args:
            task: The task to send
            
        Returns:
            True if task was sent successfully, False otherwise
        """
        if not self.connected_fog_node:
            print(f"❌ {self.device_id}: No fog node connected, cannot send task {task.task_id}")
            self.tasks_failed += 1
            return False
        
        try:
            # Simulate network latency based on distance
            distance = self.location.distance_to(self.connected_fog_node.location)
            network_latency = distance * 0.01  # 0.01 time units per distance unit
            
            # Update task with network information
            task.network_latency = network_latency
            task.transmission_time = self.env.now + network_latency
            
            # Send task to fog node
            self.connected_fog_node.receive_task(task)
            self.tasks_sent += 1
            
            print(f"📤 {self.device_id}: Sent task {task.task_id} to {self.connected_fog_node.node_id} "
                  f"(latency: {network_latency:.3f}s)")
            return True
            
        except Exception as e:
            print(f"❌ {self.device_id}: Failed to send task {task.task_id}: {e}")
            self.tasks_failed += 1
            return False
    
    def task_generation_process(self):
        """
        SimPy process that continuously generates tasks at random intervals.
        This method should be started as a SimPy process.
        """
        while True:
            try:
                # Wait for next task generation
                inter_arrival_time = random.expovariate(self.task_generation_rate)
                yield self.env.timeout(inter_arrival_time)
                
                # Generate and send task
                task = self.generate_task()
                self.send_task_to_fog(task)
                
            except Exception as e:
                print(f"❌ {self.device_id}: Error in task generation process: {e}")
                yield self.env.timeout(1.0)  # Wait before retrying


class FogNode:
    """
    Represents a fog node in the fog computing network.
    
    Fog nodes provide intermediate processing capabilities between IoT devices
    and the cloud server. They have moderate computational resources and can
    offload tasks to the cloud when necessary.
    """
    
    def __init__(self, node_id: str, location: Location, 
                 computational_resources: ComputationalResources,
                 cloud_server: Optional['CloudServer'] = None, env: Optional[simpy.Environment] = None):
        """
        Initialize a fog node.
        
        Args:
            node_id: Unique identifier for the fog node
            location: Physical location of the fog node
            computational_resources: Available computational resources
            cloud_server: Reference to the central cloud server
            env: SimPy environment for task processing
        """
        self.node_id = node_id
        self.location = location
        self.computational_resources = computational_resources
        self.connected_cloud_server = cloud_server
        self.device_type = DeviceType.FOG_NODE
        self.env = env
        
        # SimPy resource for processing capacity
        self.processing_capacity = None  # Will be set by the simulation environment
        self.connected_iot_devices: List[IoTDevice] = []
        
        # Task processing statistics
        self.tasks_processed = 0
        self.tasks_offloaded = 0
        self.tasks_failed = 0
        self.total_processing_time = 0.0
        self.pending_tasks: List[Task] = []
        
        # Offloading decision parameters
        self.cloud_latency = 5.0  # Predefined cloud network latency
        self.complexity_threshold = 1000.0  # MIPS threshold for offloading
        self.utilization_threshold = 0.8  # CPU utilization threshold
        self.deadline_threshold = 5.0  # Time units before deadline
        
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
    
    def decision_engine(self, task: Task) -> tuple[OffloadDecision, str]:
        """
        Intelligent decision engine for task offloading.
        
        Analyzes task characteristics and node state to decide whether to process
        locally or offload to cloud.
        
        Args:
            task: The task to be processed
            
        Returns:
            Tuple of (decision, reason)
        """
        current_time = self.env.now
        current_utilization = self.get_utilization()
        time_to_deadline = task.deadline - current_time
        
        # Decision factors
        factors = {
            'task_complexity': task.complexity_mips,
            'cpu_utilization': current_utilization,
            'time_to_deadline': time_to_deadline,
            'queue_length': len(self.pending_tasks)
        }
        
        # Rule-based decision logic
        reasons = []
        
        # Factor 1: Task complexity
        if task.complexity_mips > self.complexity_threshold:
            reasons.append(f"High complexity ({task.complexity_mips:.0f} > {self.complexity_threshold:.0f} MIPS)")
        
        # Factor 2: CPU utilization
        if current_utilization > self.utilization_threshold:
            reasons.append(f"High CPU utilization ({current_utilization:.1%} > {self.utilization_threshold:.1%})")
        
        # Factor 3: Tight deadline
        if time_to_deadline < self.deadline_threshold:
            reasons.append(f"Tight deadline ({time_to_deadline:.1f}s < {self.deadline_threshold:.1f}s)")
        
        # Factor 4: Queue length
        if len(self.pending_tasks) > 5:
            reasons.append(f"Long queue ({len(self.pending_tasks)} tasks)")
        
        # Decision logic: Offload if any critical factor is met
        if reasons:
            decision = OffloadDecision.OFFLOAD_TO_CLOUD
            reason = f"Offload due to: {', '.join(reasons)}"
        else:
            decision = OffloadDecision.PROCESS_LOCALLY
            reason = f"Process locally - complexity: {task.complexity_mips:.0f} MIPS, utilization: {current_utilization:.1%}, deadline: {time_to_deadline:.1f}s"
        
        return decision, reason
    
    def receive_task(self, task: Task):
        """
        Receive a task from an IoT device and add it to the processing queue.
        
        Args:
            task: The task to be processed
        """
        print(f"📥 {self.node_id}: Received task {task.task_id} from {task.source_device_id}")
        self.pending_tasks.append(task)
        
        # Log task arrival at fog node
        task.arrival_at_fog_time = self.env.now
        global_logger.log_task_event(
            event_type='arrival_at_fog_time',
            task_id=task.task_id,
            timestamp=self.env.now,
            task_complexity=task.complexity_mips,
            processing_location=self.node_id
        )
        
        # Start processing the task
        if self.env:
            self.env.process(self.handle_task(task))
    
    def handle_task(self, task: Task):
        """
        Handle a task by processing it locally or offloading to cloud.
        This is a SimPy process that manages task execution.
        
        Args:
            task: The task to be processed
        """
        try:
            # Check if task is overdue
            if task.is_overdue(self.env.now):
                print(f"⏰ {self.node_id}: Task {task.task_id} is overdue, marking as timeout")
                task.status = TaskStatus.TIMEOUT
                self.tasks_failed += 1
                return
            
            # Run decision engine
            decision, reason = self.decision_engine(task)
            task.offload_decision = decision
            task.offload_reason = reason
            
            # Log decision time
            task.decision_time = self.env.now
            global_logger.log_task_event(
                event_type='decision_time',
                task_id=task.task_id,
                timestamp=self.env.now,
                task_complexity=task.complexity_mips,
                decision_made=decision.value,
                processing_location=self.node_id,
                additional_data={'reason': reason}
            )
            
            print(f"🧠 {self.node_id}: Decision for task {task.task_id}: {decision.value}")
            print(f"   Reason: {reason}")
            
            if decision == OffloadDecision.OFFLOAD_TO_CLOUD:
                # Offload to cloud
                self.offload_task_to_cloud(task)
            else:
                # Process locally
                yield from self.process_task_locally(task)
                
        except Exception as e:
            print(f"❌ {self.node_id}: Error processing task {task.task_id}: {e}")
            task.status = TaskStatus.FAILED
            self.tasks_failed += 1
    
    def offload_task_to_cloud(self, task: Task):
        """
        Offload a task to the cloud server.
        
        Args:
            task: The task to be offloaded
        """
        if not self.connected_cloud_server:
            print(f"❌ {self.node_id}: No cloud server connected, cannot offload task {task.task_id}")
            task.status = TaskStatus.FAILED
            self.tasks_failed += 1
            return
        
        try:
            # Set offload decision
            task.offload_decision = OffloadDecision.OFFLOAD_TO_CLOUD
            
            # Simulate network latency to cloud
            distance = self.location.distance_to(self.connected_cloud_server.location)
            cloud_latency = distance * 0.02 + self.cloud_latency  # Additional cloud latency
            
            # Update task with cloud transmission information
            task.cloud_network_latency = cloud_latency
            task.cloud_transmission_time = self.env.now + cloud_latency
            
            # Send task to cloud server
            self.connected_cloud_server.receive_task(task)
            self.tasks_offloaded += 1
            
            print(f"☁️ {self.node_id}: Offloaded task {task.task_id} to cloud "
                  f"(latency: {cloud_latency:.3f}s)")
            
        except Exception as e:
            print(f"❌ {self.node_id}: Failed to offload task {task.task_id}: {e}")
            task.status = TaskStatus.FAILED
            self.tasks_failed += 1
    
    def process_task_locally(self, task: Task):
        """
        Process a task locally on the fog node.
        
        Args:
            task: The task to be processed
        """
        # Request CPU resource
        print(f"🔄 {self.node_id}: Starting local processing of task {task.task_id}")
        task.status = TaskStatus.PROCESSING
        task.start_time = self.env.now
        task.processing_node = self.node_id
        
        # Log processing start time
        task.processing_start_time = self.env.now
        global_logger.log_task_event(
            event_type='processing_start_time',
            task_id=task.task_id,
            timestamp=self.env.now,
            task_complexity=task.complexity_mips,
            decision_made=task.offload_decision.value if task.offload_decision else None,
            processing_location=self.node_id
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
                decision_made=task.offload_decision.value if task.offload_decision else None,
                processing_location=self.node_id,
                additional_data={'processing_time': processing_time}
            )
            
            # Update statistics
            self.tasks_processed += 1
            self.total_processing_time += processing_time
            
            print(f"✅ {self.node_id}: Completed task {task.task_id} locally "
                  f"(processing time: {processing_time:.3f}s, "
                  f"total time: {task.get_response_time():.3f}s)")
    
    def get_task_statistics(self) -> dict:
        """Get comprehensive task processing statistics."""
        return {
            'tasks_processed': self.tasks_processed,
            'tasks_offloaded': self.tasks_offloaded,
            'tasks_failed': self.tasks_failed,
            'total_processing_time': self.total_processing_time,
            'average_processing_time': (self.total_processing_time / self.tasks_processed 
                                      if self.tasks_processed > 0 else 0.0),
            'pending_tasks': len(self.pending_tasks),
            'utilization': self.get_utilization()
        }


class CloudServer:
    """
    Represents the central cloud server in the fog computing network.
    
    The cloud server has significantly more computational resources than fog nodes
    and can handle complex tasks that cannot be processed at the fog level.
    """
    
    def __init__(self, server_id: str, location: Location, 
                 computational_resources: ComputationalResources, env: Optional[simpy.Environment] = None):
        """
        Initialize a cloud server.
        
        Args:
            server_id: Unique identifier for the cloud server
            location: Physical location of the cloud server
            computational_resources: Available computational resources
            env: SimPy environment for task processing
        """
        self.server_id = server_id
        self.location = location
        self.computational_resources = computational_resources
        self.device_type = DeviceType.CLOUD_SERVER
        self.env = env
        
        # SimPy resource for processing capacity
        self.processing_capacity = None  # Will be set by the simulation environment
        
        # Performance metrics
        self.tasks_processed = 0
        self.tasks_failed = 0
        self.total_processing_time = 0.0
        self.pending_tasks: List[Task] = []
        
    def __str__(self):
        return f"Cloud Server {self.server_id} at {self.location} with {self.computational_resources}"
    
    def receive_task(self, task: Task):
        """
        Receive a task from a fog node and add it to the processing queue.
        
        Args:
            task: The task to be processed
        """
        print(f"☁️ {self.server_id}: Received offloaded task {task.task_id} from fog node")
        self.pending_tasks.append(task)
        
        # Log task arrival at cloud server
        global_logger.log_task_event(
            event_type='arrival_at_cloud_time',
            task_id=task.task_id,
            timestamp=self.env.now,
            task_complexity=task.complexity_mips,
            decision_made=task.offload_decision.value if task.offload_decision else None,
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
                decision_made=task.offload_decision.value if task.offload_decision else None,
                processing_location=self.server_id
            )
            
            with self.processing_capacity.request() as cpu_request:
                # Wait for CPU resource
                yield cpu_request
                
                # Calculate processing time (cloud has higher CPU capacity)
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
                    decision_made=task.offload_decision.value if task.offload_decision else None,
                    processing_location=self.server_id,
                    additional_data={'processing_time': processing_time}
                )
                
                # Update statistics
                self.tasks_processed += 1
                self.total_processing_time += processing_time
                
                print(f"✅ {self.server_id}: Completed offloaded task {task.task_id} "
                      f"(processing time: {processing_time:.3f}s, "
                      f"total time: {task.get_response_time():.3f}s)")
                
        except Exception as e:
            print(f"❌ {self.server_id}: Error processing task {task.task_id}: {e}")
            task.status = TaskStatus.FAILED
            self.tasks_failed += 1
    
    def get_utilization(self) -> float:
        """Calculate current resource utilization."""
        if self.processing_capacity:
            return 1.0 - (self.processing_capacity.capacity - self.processing_capacity.count) / self.processing_capacity.capacity
        return 0.0
    
    def get_task_statistics(self) -> dict:
        """Get comprehensive task processing statistics."""
        return {
            'tasks_processed': self.tasks_processed,
            'tasks_failed': self.tasks_failed,
            'total_processing_time': self.total_processing_time,
            'average_processing_time': (self.total_processing_time / self.tasks_processed 
                                      if self.tasks_processed > 0 else 0.0),
            'pending_tasks': len(self.pending_tasks),
            'utilization': self.get_utilization()
        }


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
            ),
            env=self.env
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
                cloud_server=self.cloud_server,
                env=self.env
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
                ),
                env=self.env
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
    
    def start_task_generation(self):
        """Start task generation processes for all IoT devices."""
        print("\n🔄 Starting Task Generation Processes...")
        
        for iot_device in self.iot_devices:
            # Start task generation process for each IoT device
            self.env.process(iot_device.task_generation_process())
            print(f"   ✓ Started task generation for {iot_device.device_id}")
    
    def resource_monitoring_process(self):
        """
        SimPy process that periodically monitors and logs resource utilization.
        """
        while True:
            # Monitor fog nodes
            for fog_node in self.fog_nodes:
                utilization = fog_node.get_utilization()
                queue_length = len(fog_node.pending_tasks)
                capacity = fog_node.processing_capacity.capacity if fog_node.processing_capacity else 0
                
                global_logger.log_resource_utilization(
                    timestamp=self.env.now,
                    node_id=fog_node.node_id,
                    utilization=utilization,
                    queue_length=queue_length,
                    processing_capacity=capacity,
                    node_type='fog'
                )
            
            # Monitor cloud server
            cloud_utilization = self.cloud_server.get_utilization()
            cloud_queue_length = len(self.cloud_server.pending_tasks)
            cloud_capacity = self.cloud_server.processing_capacity.capacity if self.cloud_server.processing_capacity else 0
            
            global_logger.log_resource_utilization(
                timestamp=self.env.now,
                node_id=self.cloud_server.server_id,
                utilization=cloud_utilization,
                queue_length=cloud_queue_length,
                processing_capacity=cloud_capacity,
                node_type='cloud'
            )
            
            # Wait before next monitoring cycle
            yield self.env.timeout(1.0)  # Monitor every 1 simulation time unit
    
    def run_simulation(self):
        """Run the simulation for the specified duration."""
        print(f"\n🚀 Starting Simulation for {self.simulation_time} seconds...")
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
        
        print(f"✅ Simulation completed in {self.end_time - self.start_time:.2f} seconds")
    
    def print_simulation_results(self):
        """Print comprehensive simulation results and statistics."""
        print("\n📊 Simulation Results")
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
        
        # Fog node statistics
        print(f"\n🌫️  Fog Node Statistics:")
        for i, fog_node in enumerate(self.fog_nodes, 1):
            stats = fog_node.get_task_statistics()
            print(f"   Fog Node {i} ({fog_node.node_id}):")
            print(f"      Tasks processed locally: {stats['tasks_processed']}")
            print(f"      Tasks offloaded to cloud: {stats['tasks_offloaded']}")
            print(f"      Tasks failed: {stats['tasks_failed']}")
            print(f"      Average processing time: {stats['average_processing_time']:.3f}s")
            print(f"      Resource utilization: {stats['utilization']:.1%}")
            print(f"      Pending tasks: {stats['pending_tasks']}")
        
        # Cloud server statistics
        print(f"\n☁️  Cloud Server Statistics:")
        cloud_stats = self.cloud_server.get_task_statistics()
        print(f"   Cloud Server ({self.cloud_server.server_id}):")
        print(f"      Tasks processed: {cloud_stats['tasks_processed']}")
        print(f"      Tasks failed: {cloud_stats['tasks_failed']}")
        print(f"      Average processing time: {cloud_stats['average_processing_time']:.3f}s")
        print(f"      Resource utilization: {cloud_stats['utilization']:.1%}")
        print(f"      Pending tasks: {cloud_stats['pending_tasks']}")
        
        # Overall network statistics
        total_fog_processed = sum(fog.tasks_processed for fog in self.fog_nodes)
        total_fog_offloaded = sum(fog.tasks_offloaded for fog in self.fog_nodes)
        total_fog_failed = sum(fog.tasks_failed for fog in self.fog_nodes)
        total_cloud_processed = self.cloud_server.tasks_processed
        total_cloud_failed = self.cloud_server.tasks_failed
        
        print(f"\n🌐 Network Performance:")
        print(f"   Total tasks processed by fog nodes: {total_fog_processed}")
        print(f"   Total tasks offloaded to cloud: {total_fog_offloaded}")
        print(f"   Total tasks processed by cloud: {total_cloud_processed}")
        print(f"   Total tasks failed: {total_fog_failed + total_cloud_failed}")
        print(f"   Offloading rate: {(total_fog_offloaded / (total_fog_processed + total_fog_offloaded) * 100):.1f}%" if (total_fog_processed + total_fog_offloaded) > 0 else "   Offloading rate: 0%")
        print(f"   Overall processing success rate: {((total_fog_processed + total_cloud_processed) / (total_fog_processed + total_fog_offloaded + total_fog_failed + total_cloud_failed) * 100):.1f}%" if (total_fog_processed + total_fog_offloaded + total_fog_failed + total_cloud_failed) > 0 else "   Overall processing success rate: 0%")
        
        # Calculate average response time
        all_tasks = []
        for fog in self.fog_nodes:
            all_tasks.extend(fog.pending_tasks)
        
        completed_tasks = [task for task in all_tasks if task.status == TaskStatus.COMPLETED]
        if completed_tasks:
            avg_response_time = sum(task.get_response_time() for task in completed_tasks) / len(completed_tasks)
            print(f"   Average response time: {avg_response_time:.3f}s")
        
        print(f"\n⏱️  Simulation Duration: {self.end_time - self.start_time:.2f} seconds")
        
        # Print performance monitoring summary
        print(f"\n📈 Performance Monitoring Summary:")
        performance_summary = global_logger.get_performance_summary()
        if performance_summary:
            print(f"   Total events logged: {performance_summary.get('total_events', 0)}")
            print(f"   Total tasks tracked: {performance_summary.get('total_tasks', 0)}")
            print(f"   Average response time: {performance_summary.get('average_response_time', 0):.3f}s")
            print(f"   Average processing time: {performance_summary.get('average_processing_time', 0):.3f}s")
            print(f"   Average decision time: {performance_summary.get('average_decision_time', 0):.3f}s")
            print(f"   Resource monitoring entries: {performance_summary.get('resource_monitoring_entries', 0)}")
        
        print(f"\n🎉 Simulation setup and execution completed successfully!")
        print("✅ Task generation and processing logic implemented!")
        print("✅ Performance monitoring and data logging implemented!")
    
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
    
    # Print results
    simulation.print_simulation_results()
    
    print("\n🎉 Simulation setup and execution completed successfully!")
    print("✅ Task generation and processing logic implemented!")


if __name__ == "__main__":
    main()
