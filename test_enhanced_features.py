"""
Test Enhanced Features
======================

This script demonstrates the enhanced fog computing simulation features
including configuration management, node failure simulation, and advanced
robustness capabilities.
"""

import sys
import os
import time
import json

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config_manager import ConfigManager, create_default_config
from enhanced_fog_simulation import EnhancedFogComputingSimulation


def test_configuration_management():
    """Test configuration management functionality."""
    print("🧪 Testing Configuration Management...")
    
    try:
        # Test configuration loading
        config_manager = ConfigManager()
        config_manager.print_config_summary()
        
        # Test configuration access
        sim_config = config_manager.get_simulation_config()
        network_config = config_manager.get_network_topology_config()
        task_config = config_manager.get_task_generation_config()
        
        print(f"   ✓ Simulation duration: {sim_config.duration}s")
        print(f"   ✓ Fog nodes: {network_config.num_fog_nodes}")
        print(f"   ✓ IoT devices: {network_config.num_iot_devices}")
        print(f"   ✓ Task complexity range: {task_config.complexity_range}")
        print("   ✅ Configuration management test passed!\n")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Configuration management test failed: {e}")
        return False


def test_enhanced_simulation():
    """Test enhanced simulation with configuration and failure simulation."""
    print("🧪 Testing Enhanced Simulation...")
    
    try:
        # Create enhanced simulation
        simulation = EnhancedFogComputingSimulation()
        
        # Setup simulation
        simulation.setup_simulation()
        
        # Verify enhanced components
        assert len(simulation.enhanced_fog_nodes) > 0, "No enhanced fog nodes created"
        assert len(simulation.enhanced_iot_devices) > 0, "No enhanced IoT devices created"
        assert simulation.cloud_server is not None, "No cloud server created"
        
        print(f"   ✓ Enhanced fog nodes: {len(simulation.enhanced_fog_nodes)}")
        print(f"   ✓ Enhanced IoT devices: {len(simulation.enhanced_iot_devices)}")
        print(f"   ✓ Cloud server: {simulation.cloud_server.server_id}")
        
        # Test node status
        operational_nodes = [node for node in simulation.enhanced_fog_nodes if node.is_operational()]
        print(f"   ✓ Operational nodes: {len(operational_nodes)}")
        
        # Test failure simulation setup
        if simulation.sim_config.enable_node_failures:
            print(f"   ✓ Node failure simulation enabled")
            print(f"   ✓ Failure probability: {simulation.sim_config.failure_probability}")
        
        print("   ✅ Enhanced simulation test passed!\n")
        return True
        
    except Exception as e:
        print(f"   ❌ Enhanced simulation test failed: {e}")
        return False


def test_node_failure_simulation():
    """Test node failure simulation functionality."""
    print("🧪 Testing Node Failure Simulation...")
    
    try:
        # Create simulation with failures enabled
        simulation = EnhancedFogComputingSimulation()
        simulation.setup_simulation()
        
        # Test node failure
        fog_node = simulation.enhanced_fog_nodes[0]
        initial_status = fog_node.status
        
        # Simulate failure
        failure_duration = 10.0
        fog_node.simulate_failure(simulation.env.now, failure_duration)
        
        # Verify failure state
        assert fog_node.status.value == "failed", "Node should be in failed state"
        assert not fog_node.is_operational(), "Node should not be operational"
        assert fog_node.current_failure is not None, "Should have current failure record"
        
        print(f"   ✓ Node failure simulated: {fog_node.node_id}")
        print(f"   ✓ Failure duration: {failure_duration}s")
        print(f"   ✓ Node status: {fog_node.status.value}")
        
        # Test recovery
        fog_node.recover_from_failure(simulation.env.now + failure_duration)
        
        # Verify recovery
        assert fog_node.status.value == "operational", "Node should be operational after recovery"
        assert fog_node.is_operational(), "Node should be operational"
        assert fog_node.current_failure is None, "Should not have current failure"
        
        print(f"   ✓ Node recovery simulated")
        print(f"   ✓ Node status after recovery: {fog_node.status.value}")
        print("   ✅ Node failure simulation test passed!\n")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Node failure simulation test failed: {e}")
        return False


def test_rerouting_logic():
    """Test rerouting logic when fog nodes fail."""
    print("🧪 Testing Rerouting Logic...")
    
    try:
        # Create simulation
        simulation = EnhancedFogComputingSimulation()
        simulation.setup_simulation()
        
        # Test IoT device rerouting
        iot_device = simulation.enhanced_iot_devices[0]
        primary_fog = iot_device.primary_fog_node
        
        # Simulate primary fog node failure
        primary_fog.simulate_failure(simulation.env.now, 20.0)
        
        # Test finding operational fog node
        operational_fog = iot_device.find_operational_fog_node()
        
        if operational_fog:
            print(f"   ✓ Found alternative fog node: {operational_fog.node_id}")
        else:
            print(f"   ✓ No operational fog nodes, will route to cloud")
        
        # Test cloud routing capability
        assert iot_device.cloud_server is not None, "IoT device should have cloud server reference"
        
        print(f"   ✓ Cloud server available: {iot_device.cloud_server.server_id}")
        print("   ✅ Rerouting logic test passed!\n")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Rerouting logic test failed: {e}")
        return False


def test_short_simulation():
    """Test short simulation with enhanced features."""
    print("🧪 Testing Short Enhanced Simulation...")
    
    try:
        # Create simulation with shorter duration
        simulation = EnhancedFogComputingSimulation()
        
        # Modify simulation duration for testing
        simulation.simulation_time = 10.0
        simulation.setup_simulation()
        
        print(f"   ✓ Running simulation for {simulation.simulation_time}s...")
        
        # Run simulation
        start_time = time.time()
        simulation.run_simulation()
        end_time = time.time()
        
        print(f"   ✓ Simulation completed in {end_time - start_time:.2f}s")
        
        # Check results
        total_tasks = sum(device.tasks_generated for device in simulation.enhanced_iot_devices)
        print(f"   ✓ Total tasks generated: {total_tasks}")
        
        # Check failure events
        if simulation.failure_events:
            print(f"   ✓ Node failures occurred: {len(simulation.failure_events)}")
            for failure in simulation.failure_events:
                print(f"      {failure.node_id}: {failure.failure_time:.2f}s - {failure.recovery_time:.2f}s")
        
        print("   ✅ Short enhanced simulation test passed!\n")
        return True
        
    except Exception as e:
        print(f"   ❌ Short enhanced simulation test failed: {e}")
        return False


def test_configuration_validation():
    """Test configuration validation and error handling."""
    print("🧪 Testing Configuration Validation...")
    
    try:
        # Test with invalid configuration file
        try:
            invalid_config = ConfigManager("nonexistent_config.json")
            print("   ❌ Should have failed with nonexistent config file")
            return False
        except FileNotFoundError:
            print("   ✓ Correctly handled nonexistent config file")
        
        # Test with malformed JSON
        with open("test_invalid_config.json", "w") as f:
            f.write("{ invalid json }")
        
        try:
            invalid_config = ConfigManager("test_invalid_config.json")
            print("   ❌ Should have failed with malformed JSON")
            return False
        except json.JSONDecodeError:
            print("   ✓ Correctly handled malformed JSON")
        
        # Clean up test file
        if os.path.exists("test_invalid_config.json"):
            os.remove("test_invalid_config.json")
        
        print("   ✅ Configuration validation test passed!\n")
        return True
        
    except Exception as e:
        print(f"   ❌ Configuration validation test failed: {e}")
        return False


def run_all_enhanced_tests():
    """Run all enhanced feature tests."""
    print("🚀 Running Enhanced Features Tests")
    print("=" * 60)
    
    tests = [
        test_configuration_management,
        test_enhanced_simulation,
        test_node_failure_simulation,
        test_rerouting_logic,
        test_short_simulation,
        test_configuration_validation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All enhanced features tests passed successfully!")
        print("✅ Enhanced fog computing simulation is working correctly.")
        return True
    else:
        print(f"❌ {total - passed} tests failed.")
        return False


def main():
    """Main function to run enhanced features tests."""
    print("🌐 Enhanced Fog Computing Simulation - Feature Testing")
    print("=" * 70)
    
    # Ensure configuration file exists
    if not os.path.exists("config.json"):
        print("Creating default configuration file...")
        create_default_config()
    
    # Run all tests
    success = run_all_enhanced_tests()
    
    if success:
        print("\n🎯 Enhanced Features Summary:")
        print("   ✅ Configuration Management")
        print("   ✅ Node Failure Simulation")
        print("   ✅ Rerouting Logic")
        print("   ✅ Enhanced Error Handling")
        print("   ✅ Robustness Features")
        print("\n🚀 Ready for advanced fog computing simulations!")
    else:
        print("\n❌ Some tests failed. Please check the implementation.")
    
    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
