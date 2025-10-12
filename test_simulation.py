"""
Test script for the Fog Computing Simulation Environment
======================================================

This script tests the basic functionality of the simulation environment
and verifies that all components are properly initialized and connected.
"""

import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fog_simulation import (
    FogComputingSimulation, 
    Location, 
    ComputationalResources,
    IoTDevice,
    FogNode,
    CloudServer
)


def test_basic_components():
    """Test basic component creation and initialization."""
    print("🧪 Testing Basic Component Creation...")
    
    # Test Location class
    loc1 = Location(10, 20)
    loc2 = Location(15, 25)
    distance = loc1.distance_to(loc2)
    print(f"   ✓ Location distance calculation: {distance:.2f}")
    
    # Test ComputationalResources
    resources = ComputationalResources(cpu_mips=1000, memory=2000, storage=5000)
    print(f"   ✓ ComputationalResources: {resources}")
    
    # Test CloudServer creation
    cloud = CloudServer("TEST_CLOUD", Location(50, 50), resources)
    print(f"   ✓ CloudServer created: {cloud.server_id}")
    
    # Test FogNode creation
    fog = FogNode("TEST_FOG", Location(30, 30), resources, cloud)
    print(f"   ✓ FogNode created: {fog.node_id}")
    
    # Test IoTDevice creation
    iot = IoTDevice("TEST_IOT", Location(25, 25), resources, fog)
    print(f"   ✓ IoTDevice created: {iot.device_id}")
    
    print("   ✅ All basic components created successfully!\n")


def test_network_topology():
    """Test network topology creation and connections."""
    print("🧪 Testing Network Topology...")
    
    # Create simulation environment
    simulation = FogComputingSimulation(simulation_time=10.0)
    
    # Setup with small network
    simulation.setup_simulation(num_fog_nodes=2, num_iot_devices=5)
    
    # Verify cloud server exists
    assert simulation.cloud_server is not None, "Cloud server not created"
    print("   ✓ Cloud server created")
    
    # Verify fog nodes exist
    assert len(simulation.fog_nodes) == 2, f"Expected 2 fog nodes, got {len(simulation.fog_nodes)}"
    print("   ✓ Fog nodes created")
    
    # Verify IoT devices exist
    assert len(simulation.iot_devices) == 5, f"Expected 5 IoT devices, got {len(simulation.iot_devices)}"
    print("   ✓ IoT devices created")
    
    # Verify connections
    for iot in simulation.iot_devices:
        assert iot.connected_fog_node is not None, f"IoT device {iot.device_id} not connected to fog node"
    print("   ✓ IoT devices connected to fog nodes")
    
    for fog in simulation.fog_nodes:
        assert fog.connected_cloud_server is not None, f"Fog node {fog.node_id} not connected to cloud"
    print("   ✓ Fog nodes connected to cloud server")
    
    # Verify SimPy resources initialized
    assert simulation.cloud_server.processing_capacity is not None, "Cloud processing capacity not initialized"
    for fog in simulation.fog_nodes:
        assert fog.processing_capacity is not None, f"Fog node {fog.node_id} processing capacity not initialized"
    print("   ✓ SimPy resources initialized")
    
    print("   ✅ Network topology test passed!\n")


def test_simulation_execution():
    """Test basic simulation execution."""
    print("🧪 Testing Simulation Execution...")
    
    # Create and setup simulation
    simulation = FogComputingSimulation(simulation_time=5.0)
    simulation.setup_simulation(num_fog_nodes=2, num_iot_devices=3)
    
    # Run simulation
    initial_time = simulation.env.now
    simulation.run_simulation()
    final_time = simulation.env.now
    
    # Verify simulation ran
    assert final_time >= initial_time, "Simulation time did not advance"
    print(f"   ✓ Simulation executed for {final_time - initial_time:.2f} seconds")
    
    print("   ✅ Simulation execution test passed!\n")


def test_performance_metrics():
    """Test performance metrics and statistics."""
    print("🧪 Testing Performance Metrics...")
    
    # Create simulation
    simulation = FogComputingSimulation(simulation_time=10.0)
    simulation.setup_simulation(num_fog_nodes=3, num_iot_devices=8)
    
    # Test resource utilization calculation
    for fog in simulation.fog_nodes:
        utilization = fog.get_utilization()
        assert 0.0 <= utilization <= 1.0, f"Invalid utilization value: {utilization}"
    print("   ✓ Resource utilization calculation works")
    
    # Test network statistics
    total_devices = len(simulation.iot_devices) + len(simulation.fog_nodes) + 1
    expected_devices = 8 + 3 + 1  # IoT + Fog + Cloud
    assert total_devices == expected_devices, f"Expected {expected_devices} devices, got {total_devices}"
    print("   ✓ Network statistics calculation works")
    
    # Test capacity calculations
    total_fog_capacity = sum(fog.processing_capacity.capacity for fog in simulation.fog_nodes)
    cloud_capacity = simulation.cloud_server.processing_capacity.capacity
    assert total_fog_capacity > 0, "Total fog capacity should be positive"
    assert cloud_capacity > 0, "Cloud capacity should be positive"
    print("   ✓ Capacity calculations work")
    
    print("   ✅ Performance metrics test passed!\n")


def run_all_tests():
    """Run all test functions."""
    print("🚀 Running Fog Computing Simulation Tests")
    print("=" * 50)
    
    try:
        test_basic_components()
        test_network_topology()
        test_simulation_execution()
        test_performance_metrics()
        
        print("🎉 All tests passed successfully!")
        print("✅ The fog computing simulation environment is working correctly.")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
