"""
Example Usage of Fog Computing Simulation
========================================

This script demonstrates how to use the fog computing simulation environment
with different configurations and scenarios.
"""

from fog_simulation import FogComputingSimulation, Location, ComputationalResources


def example_basic_simulation():
    """Example: Basic simulation with default parameters."""
    print("📋 Example 1: Basic Simulation")
    print("-" * 40)
    
    # Create simulation with default parameters
    simulation = FogComputingSimulation(simulation_time=50.0)
    
    # Setup network topology
    simulation.setup_simulation(
        num_fog_nodes=3,
        num_iot_devices=8
    )
    
    # Run simulation
    simulation.run_simulation()
    print("✅ Basic simulation completed!\n")


def example_large_network():
    """Example: Large network simulation."""
    print("📋 Example 2: Large Network Simulation")
    print("-" * 40)
    
    # Create simulation for larger network
    simulation = FogComputingSimulation(simulation_time=100.0)
    
    # Setup with more devices
    simulation.setup_simulation(
        num_fog_nodes=5,
        num_iot_devices=20
    )
    
    # Run simulation
    simulation.run_simulation()
    print("✅ Large network simulation completed!\n")


def example_custom_resources():
    """Example: Custom resource configuration."""
    print("📋 Example 3: Custom Resource Configuration")
    print("-" * 40)
    
    # Create simulation
    simulation = FogComputingSimulation(simulation_time=30.0)
    
    # Setup network
    simulation.setup_simulation(num_fog_nodes=2, num_iot_devices=6)
    
    # Customize cloud server resources
    simulation.cloud_server.computational_resources = ComputationalResources(
        cpu_mips=15000,  # 15,000 MIPS
        memory=64000,    # 64 GB
        storage=2000000  # 2 TB
    )
    
    # Customize fog node resources
    for fog in simulation.fog_nodes:
        fog.computational_resources = ComputationalResources(
            cpu_mips=5000,   # 5,000 MIPS
            memory=16000,    # 16 GB
            storage=1000000  # 1 TB
        )
    
    print("   Custom resources configured:")
    print(f"   Cloud: {simulation.cloud_server.computational_resources}")
    print(f"   Fog Nodes: {simulation.fog_nodes[0].computational_resources}")
    
    # Run simulation
    simulation.run_simulation()
    print("✅ Custom resource simulation completed!\n")


def example_network_analysis():
    """Example: Network analysis and statistics."""
    print("📋 Example 4: Network Analysis")
    print("-" * 40)
    
    # Create simulation
    simulation = FogComputingSimulation(simulation_time=20.0)
    simulation.setup_simulation(num_fog_nodes=4, num_iot_devices=15)
    
    # Analyze network topology
    print("   Network Analysis:")
    print(f"   Total devices: {len(simulation.iot_devices) + len(simulation.fog_nodes) + 1}")
    print(f"   IoT devices per fog node: {len(simulation.iot_devices) / len(simulation.fog_nodes):.1f}")
    
    # Calculate total processing capacity
    total_fog_capacity = sum(fog.processing_capacity.capacity for fog in simulation.fog_nodes)
    cloud_capacity = simulation.cloud_server.processing_capacity.capacity
    print(f"   Total fog capacity: {total_fog_capacity}")
    print(f"   Cloud capacity: {cloud_capacity}")
    print(f"   Fog-to-cloud ratio: {total_fog_capacity / cloud_capacity:.2f}")
    
    # Analyze device distribution
    print("\n   Device Distribution:")
    for i, fog in enumerate(simulation.fog_nodes, 1):
        iot_count = len(fog.connected_iot_devices)
        print(f"   Fog Node {i}: {iot_count} IoT devices")
    
    # Run simulation
    simulation.run_simulation()
    print("✅ Network analysis completed!\n")


def main():
    """Run all example scenarios."""
    print("🌐 Fog Computing Simulation Examples")
    print("=" * 50)
    print("Demonstrating different simulation scenarios...\n")
    
    try:
        example_basic_simulation()
        example_large_network()
        example_custom_resources()
        example_network_analysis()
        
        print("🎉 All examples completed successfully!")
        print("The fog computing simulation environment is ready for advanced scenarios.")
        
    except Exception as e:
        print(f"❌ Example failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
