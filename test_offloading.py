"""
Test script for Dynamic Task Offloading Engine
============================================

This script tests the intelligent task offloading functionality
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
    OffloadDecision,
    Location, 
    ComputationalResources,
    FogNode,
    CloudServer
)


def test_offload_decision_engine():
    """Test the decision engine logic."""
    print("🧪 Testing Offload Decision Engine...")
    
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
    
    # Test case 1: High complexity task
    high_complexity_task = Task(
        task_id="HIGH_COMPLEXITY",
        creation_time=0.0,
        complexity_mips=1500.0,  # Above threshold
        deadline=20.0,
        source_device_id="TEST_IOT"
    )
    
    decision, reason = fog_node.decision_engine(high_complexity_task)
    assert decision == OffloadDecision.OFFLOAD_TO_CLOUD, f"Expected OFFLOAD_TO_CLOUD, got {decision}"
    assert "High complexity" in reason, f"Reason should mention high complexity: {reason}"
    print("   ✓ High complexity task correctly offloaded")
    
    # Test case 2: Normal complexity task
    normal_task = Task(
        task_id="NORMAL_TASK",
        creation_time=0.0,
        complexity_mips=500.0,  # Below threshold
        deadline=20.0,
        source_device_id="TEST_IOT"
    )
    
    decision, reason = fog_node.decision_engine(normal_task)
    assert decision == OffloadDecision.PROCESS_LOCALLY, f"Expected PROCESS_LOCALLY, got {decision}"
    assert "Process locally" in reason, f"Reason should mention local processing: {reason}"
    print("   ✓ Normal complexity task correctly processed locally")
    
    # Test case 3: Tight deadline task
    tight_deadline_task = Task(
        task_id="TIGHT_DEADLINE",
        creation_time=0.0,
        complexity_mips=500.0,
        deadline=2.0,  # Very tight deadline
        source_device_id="TEST_IOT"
    )
    
    decision, reason = fog_node.decision_engine(tight_deadline_task)
    assert decision == OffloadDecision.OFFLOAD_TO_CLOUD, f"Expected OFFLOAD_TO_CLOUD, got {decision}"
    assert "Tight deadline" in reason, f"Reason should mention tight deadline: {reason}"
    print("   ✓ Tight deadline task correctly offloaded")
    
    print("   ✅ Offload decision engine test passed!\n")


def test_cloud_server_processing():
    """Test cloud server task processing."""
    print("🧪 Testing Cloud Server Processing...")
    
    # Create test environment
    import simpy
    env = simpy.Environment()
    
    # Create cloud server
    cloud_server = CloudServer(
        server_id="TEST_CLOUD",
        location=Location(50, 50),
        computational_resources=ComputationalResources(10000, 32000, 1000000),
        env=env
    )
    
    # Initialize processing capacity
    cloud_server.processing_capacity = simpy.Resource(env, capacity=10)
    
    # Create test task
    task = Task(
        task_id="CLOUD_TASK",
        creation_time=0.0,
        complexity_mips=2000.0,
        deadline=20.0,
        source_device_id="TEST_IOT"
    )
    
    # Test task receiving
    initial_pending = len(cloud_server.pending_tasks)
    cloud_server.receive_task(task)
    assert len(cloud_server.pending_tasks) == initial_pending + 1, "Task not added to cloud pending list"
    print("   ✓ Task received by cloud server")
    
    # Test cloud server statistics
    stats = cloud_server.get_task_statistics()
    assert 'tasks_processed' in stats, "Cloud statistics missing tasks_processed"
    assert 'utilization' in stats, "Cloud statistics missing utilization"
    print("   ✓ Cloud server statistics work")
    
    print("   ✅ Cloud server processing test passed!\n")


def test_offloading_simulation():
    """Test complete simulation with offloading."""
    print("🧪 Testing Offloading Simulation...")
    
    # Create simulation with short duration for testing
    simulation = FogComputingSimulation(simulation_time=10.0)
    simulation.setup_simulation(num_fog_nodes=2, num_iot_devices=5)
    
    # Verify components are created
    assert len(simulation.iot_devices) == 5, f"Expected 5 IoT devices, got {len(simulation.iot_devices)}"
    assert len(simulation.fog_nodes) == 2, f"Expected 2 fog nodes, got {len(simulation.fog_nodes)}"
    assert simulation.cloud_server is not None, "Cloud server not created"
    print("   ✓ Simulation components created")
    
    # Run simulation
    simulation.run_simulation()
    print("   ✓ Simulation executed successfully")
    
    # Check that offloading occurred
    total_offloaded = sum(fog.tasks_offloaded for fog in simulation.fog_nodes)
    total_cloud_processed = simulation.cloud_server.tasks_processed
    print(f"   ✓ Total tasks offloaded: {total_offloaded}")
    print(f"   ✓ Total tasks processed by cloud: {total_cloud_processed}")
    
    # Verify offloading statistics
    for fog in simulation.fog_nodes:
        assert hasattr(fog, 'tasks_offloaded'), f"Fog node {fog.node_id} missing offloading statistics"
        assert fog.tasks_offloaded >= 0, f"Fog node {fog.node_id} has negative offloading count"
    
    print("   ✓ Offloading statistics validated")
    
    print("   ✅ Offloading simulation test passed!\n")


def test_decision_factors():
    """Test different decision factors."""
    print("🧪 Testing Decision Factors...")
    
    # Create test environment
    import simpy
    env = simpy.Environment()
    
    # Create fog node with specific thresholds
    fog_node = FogNode(
        node_id="TEST_FOG",
        location=Location(20, 20),
        computational_resources=ComputationalResources(1000, 4000, 100000),
        env=env
    )
    
    # Set specific thresholds for testing
    fog_node.complexity_threshold = 800.0
    fog_node.utilization_threshold = 0.7
    fog_node.deadline_threshold = 3.0
    
    # Initialize processing capacity
    fog_node.processing_capacity = simpy.Resource(env, capacity=2)
    
    # Test different scenarios
    test_cases = [
        {
            'name': 'High complexity',
            'task': Task("TEST1", 0.0, 1000.0, 20.0, "IOT"),
            'expected': OffloadDecision.OFFLOAD_TO_CLOUD
        },
        {
            'name': 'Normal task',
            'task': Task("TEST2", 0.0, 500.0, 20.0, "IOT"),
            'expected': OffloadDecision.PROCESS_LOCALLY
        },
        {
            'name': 'Tight deadline',
            'task': Task("TEST3", 0.0, 500.0, 2.0, "IOT"),
            'expected': OffloadDecision.OFFLOAD_TO_CLOUD
        }
    ]
    
    for test_case in test_cases:
        decision, reason = fog_node.decision_engine(test_case['task'])
        assert decision == test_case['expected'], f"Test case '{test_case['name']}' failed: expected {test_case['expected']}, got {decision}"
        print(f"   ✓ {test_case['name']}: {decision.value}")
    
    print("   ✅ Decision factors test passed!\n")


def test_network_latency_simulation():
    """Test network latency simulation for offloading."""
    print("🧪 Testing Network Latency Simulation...")
    
    # Create test environment
    import simpy
    env = simpy.Environment()
    
    # Create fog node and cloud server
    fog_node = FogNode(
        node_id="TEST_FOG",
        location=Location(10, 10),
        computational_resources=ComputationalResources(1000, 4000, 100000),
        env=env
    )
    
    cloud_server = CloudServer(
        server_id="TEST_CLOUD",
        location=Location(50, 50),
        computational_resources=ComputationalResources(10000, 32000, 1000000),
        env=env
    )
    
    # Connect fog node to cloud
    fog_node.connected_cloud_server = cloud_server
    
    # Create task that will be offloaded
    task = Task(
        task_id="LATENCY_TEST",
        creation_time=0.0,
        complexity_mips=1500.0,  # High complexity to trigger offloading
        deadline=20.0,
        source_device_id="TEST_IOT"
    )
    
    # Test offloading
    fog_node.offload_task_to_cloud(task)
    
    # Verify task has cloud transmission information
    assert task.cloud_network_latency > 0, "Cloud network latency not set"
    assert task.cloud_transmission_time is not None, "Cloud transmission time not set"
    assert task.offload_decision == OffloadDecision.OFFLOAD_TO_CLOUD, "Task not marked for offloading"
    
    print(f"   ✓ Cloud latency: {task.cloud_network_latency:.3f}s")
    print(f"   ✓ Cloud transmission time: {task.cloud_transmission_time:.3f}s")
    
    print("   ✅ Network latency simulation test passed!\n")


def run_all_tests():
    """Run all offloading tests."""
    print("🚀 Running Dynamic Task Offloading Tests")
    print("=" * 60)
    
    try:
        test_offload_decision_engine()
        test_cloud_server_processing()
        test_offloading_simulation()
        test_decision_factors()
        test_network_latency_simulation()
        
        print("🎉 All offloading tests passed successfully!")
        print("✅ Dynamic task offloading engine is working correctly.")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
