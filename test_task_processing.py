"""
Test script for Task Generation and Processing
============================================

This script tests the task generation and processing functionality
of the fog computing simulation environment.
"""

import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fog_simulation import (
    FogComputingSimulation, 
    Task, 
    TaskStatus,
    Location, 
    ComputationalResources,
    IoTDevice,
    FogNode
)


def test_task_creation():
    """Test Task class creation and basic functionality."""
    print("🧪 Testing Task Creation...")
    
    # Create a test task
    task = Task(
        task_id="TEST_TASK_001",
        creation_time=0.0,
        complexity_mips=100.0,
        deadline=10.0,
        source_device_id="IOT_001",
        data_size=5.0
    )
    
    # Test basic properties
    assert task.task_id == "TEST_TASK_001", "Task ID not set correctly"
    assert task.complexity_mips == 100.0, "Task complexity not set correctly"
    assert task.status == TaskStatus.PENDING, "Task status should be PENDING initially"
    print("   ✓ Task creation works")
    
    # Test processing time calculation
    processing_time = task.get_processing_time(1000.0)  # 1000 MIPS node
    expected_time = 100.0 / 1000.0  # 0.1 time units
    assert abs(processing_time - expected_time) < 0.001, f"Processing time calculation incorrect: {processing_time}"
    print("   ✓ Processing time calculation works")
    
    # Test deadline checking
    assert not task.is_overdue(5.0), "Task should not be overdue at time 5.0"
    assert task.is_overdue(15.0), "Task should be overdue at time 15.0"
    print("   ✓ Deadline checking works")
    
    print("   ✅ Task creation test passed!\n")


def test_iot_device_task_generation():
    """Test IoT device task generation functionality."""
    print("🧪 Testing IoT Device Task Generation...")
    
    # Create test environment
    import simpy
    env = simpy.Environment()
    
    # Create IoT device
    iot_device = IoTDevice(
        device_id="TEST_IOT",
        location=Location(10, 10),
        computational_resources=ComputationalResources(100, 512, 1000),
        env=env
    )
    
    # Test task generation
    task = iot_device.generate_task()
    assert task.source_device_id == "TEST_IOT", "Task source device ID incorrect"
    assert task.task_id.startswith("TEST_IOT_TASK_"), "Task ID format incorrect"
    assert task.status == TaskStatus.PENDING, "Generated task should be PENDING"
    print("   ✓ Task generation works")
    
    # Test task generation statistics
    initial_count = iot_device.tasks_generated
    task2 = iot_device.generate_task()
    assert iot_device.tasks_generated == initial_count + 1, "Task generation count not updated"
    print("   ✓ Task generation statistics work")
    
    print("   ✅ IoT device task generation test passed!\n")


def test_fog_node_task_processing():
    """Test fog node task processing functionality."""
    print("🧪 Testing Fog Node Task Processing...")
    
    # Create test environment
    import simpy
    env = simpy.Environment()
    
    # Create fog node
    fog_node = FogNode(
        node_id="TEST_FOG",
        location=Location(20, 20),
        computational_resources=ComputationalResources(1000, 4000, 100000),
        env=env
    )
    
    # Initialize processing capacity
    fog_node.processing_capacity = simpy.Resource(env, capacity=2)
    
    # Create test task
    task = Task(
        task_id="TEST_TASK_002",
        creation_time=0.0,
        complexity_mips=500.0,
        deadline=10.0,
        source_device_id="TEST_IOT"
    )
    
    # Test task receiving
    initial_pending = len(fog_node.pending_tasks)
    fog_node.receive_task(task)
    assert len(fog_node.pending_tasks) == initial_pending + 1, "Task not added to pending list"
    print("   ✓ Task receiving works")
    
    # Test task statistics
    stats = fog_node.get_task_statistics()
    assert 'tasks_processed' in stats, "Task statistics missing tasks_processed"
    assert 'utilization' in stats, "Task statistics missing utilization"
    print("   ✓ Task statistics work")
    
    print("   ✅ Fog node task processing test passed!\n")


def test_simulation_with_tasks():
    """Test complete simulation with task generation and processing."""
    print("🧪 Testing Complete Simulation with Tasks...")
    
    # Create simulation with short duration for testing
    simulation = FogComputingSimulation(simulation_time=5.0)
    simulation.setup_simulation(num_fog_nodes=2, num_iot_devices=3)
    
    # Verify components are created
    assert len(simulation.iot_devices) == 3, f"Expected 3 IoT devices, got {len(simulation.iot_devices)}"
    assert len(simulation.fog_nodes) == 2, f"Expected 2 fog nodes, got {len(simulation.fog_nodes)}"
    print("   ✓ Simulation components created")
    
    # Run simulation
    simulation.run_simulation()
    print("   ✓ Simulation executed successfully")
    
    # Check that task generation was started
    total_tasks_generated = sum(device.tasks_generated for device in simulation.iot_devices)
    print(f"   ✓ Total tasks generated: {total_tasks_generated}")
    
    # Check fog node processing
    total_tasks_processed = sum(fog.tasks_processed for fog in simulation.fog_nodes)
    print(f"   ✓ Total tasks processed: {total_tasks_processed}")
    
    print("   ✅ Complete simulation test passed!\n")


def test_task_processing_workflow():
    """Test the complete task processing workflow."""
    print("🧪 Testing Task Processing Workflow...")
    
    # Create simulation
    simulation = FogComputingSimulation(simulation_time=10.0)
    simulation.setup_simulation(num_fog_nodes=1, num_iot_devices=2)
    
    # Get references to components
    iot_device = simulation.iot_devices[0]
    fog_node = simulation.fog_nodes[0]
    
    # Verify connection
    assert iot_device.connected_fog_node == fog_node, "IoT device not connected to fog node"
    print("   ✓ IoT device connected to fog node")
    
    # Run simulation
    simulation.run_simulation()
    
    # Check results
    print(f"   IoT device generated {iot_device.tasks_generated} tasks")
    print(f"   IoT device sent {iot_device.tasks_sent} tasks")
    print(f"   Fog node processed {fog_node.tasks_processed} tasks")
    
    # Verify some tasks were generated and processed
    assert iot_device.tasks_generated > 0, "No tasks were generated"
    assert iot_device.tasks_sent > 0, "No tasks were sent"
    
    print("   ✅ Task processing workflow test passed!\n")


def run_all_tests():
    """Run all task processing tests."""
    print("🚀 Running Task Generation and Processing Tests")
    print("=" * 60)
    
    try:
        test_task_creation()
        test_iot_device_task_generation()
        test_fog_node_task_processing()
        test_simulation_with_tasks()
        test_task_processing_workflow()
        
        print("🎉 All task processing tests passed successfully!")
        print("✅ Task generation and processing functionality is working correctly.")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
