"""
Example: Task Generation and Processing
=====================================

This script demonstrates the task generation and processing capabilities
of the fog computing simulation environment.
"""

from fog_simulation import FogComputingSimulation


def example_basic_task_processing():
    """Example: Basic task generation and processing."""
    print("📋 Example 1: Basic Task Processing")
    print("-" * 40)
    
    # Create simulation with moderate duration
    simulation = FogComputingSimulation(simulation_time=20.0)
    simulation.setup_simulation(num_fog_nodes=2, num_iot_devices=5)
    
    # Run simulation
    simulation.run_simulation()
    
    # Print results
    simulation.print_simulation_results()
    print("✅ Basic task processing completed!\n")


def example_high_load_simulation():
    """Example: High load simulation with many devices."""
    print("📋 Example 2: High Load Simulation")
    print("-" * 40)
    
    # Create simulation with many devices
    simulation = FogComputingSimulation(simulation_time=30.0)
    simulation.setup_simulation(num_fog_nodes=3, num_iot_devices=15)
    
    # Run simulation
    simulation.run_simulation()
    
    # Print results
    simulation.print_simulation_results()
    print("✅ High load simulation completed!\n")


def example_resource_utilization():
    """Example: Monitor resource utilization during simulation."""
    print("📋 Example 3: Resource Utilization Monitoring")
    print("-" * 40)
    
    # Create simulation
    simulation = FogComputingSimulation(simulation_time=25.0)
    simulation.setup_simulation(num_fog_nodes=2, num_iot_devices=8)
    
    # Run simulation
    simulation.run_simulation()
    
    # Detailed resource analysis
    print("\n🔍 Detailed Resource Analysis:")
    for i, fog_node in enumerate(simulation.fog_nodes, 1):
        stats = fog_node.get_task_statistics()
        print(f"   Fog Node {i} ({fog_node.node_id}):")
        print(f"      CPU Capacity: {fog_node.computational_resources.cpu_mips:.0f} MIPS")
        print(f"      Processing Capacity: {fog_node.processing_capacity.capacity}")
        print(f"      Tasks Processed: {stats['tasks_processed']}")
        print(f"      Average Processing Time: {stats['average_processing_time']:.3f}s")
        print(f"      Resource Utilization: {stats['utilization']:.1%}")
        print(f"      Pending Tasks: {stats['pending_tasks']}")
    
    print("✅ Resource utilization analysis completed!\n")


def example_task_complexity_analysis():
    """Example: Analyze task complexity and processing times."""
    print("📋 Example 4: Task Complexity Analysis")
    print("-" * 40)
    
    # Create simulation
    simulation = FogComputingSimulation(simulation_time=15.0)
    simulation.setup_simulation(num_fog_nodes=1, num_iot_devices=3)
    
    # Run simulation
    simulation.run_simulation()
    
    # Analyze task complexity
    print("\n📊 Task Complexity Analysis:")
    
    # Collect all tasks from fog nodes
    all_tasks = []
    for fog_node in simulation.fog_nodes:
        all_tasks.extend(fog_node.pending_tasks)
    
    if all_tasks:
        # Analyze task characteristics
        complexities = [task.complexity_mips for task in all_tasks]
        deadlines = [task.deadline for task in all_tasks]
        data_sizes = [task.data_size for task in all_tasks]
        
        print(f"   Total tasks analyzed: {len(all_tasks)}")
        print(f"   Average complexity: {sum(complexities) / len(complexities):.1f} MIPS")
        print(f"   Complexity range: {min(complexities):.1f} - {max(complexities):.1f} MIPS")
        print(f"   Average deadline: {sum(deadlines) / len(deadlines):.1f}s")
        print(f"   Average data size: {sum(data_sizes) / len(data_sizes):.1f} MB")
        
        # Analyze task status distribution
        status_counts = {}
        for task in all_tasks:
            status = task.status.value
            status_counts[status] = status_counts.get(status, 0) + 1
        
        print(f"\n   Task Status Distribution:")
        for status, count in status_counts.items():
            percentage = (count / len(all_tasks)) * 100
            print(f"      {status}: {count} ({percentage:.1f}%)")
    
    print("✅ Task complexity analysis completed!\n")


def example_network_performance():
    """Example: Analyze network performance and latency."""
    print("📋 Example 5: Network Performance Analysis")
    print("-" * 40)
    
    # Create simulation
    simulation = FogComputingSimulation(simulation_time=20.0)
    simulation.setup_simulation(num_fog_nodes=2, num_iot_devices=6)
    
    # Run simulation
    simulation.run_simulation()
    
    # Analyze network performance
    print("\n🌐 Network Performance Analysis:")
    
    # Calculate network statistics
    total_tasks_generated = sum(device.tasks_generated for device in simulation.iot_devices)
    total_tasks_sent = sum(device.tasks_sent for device in simulation.iot_devices)
    total_tasks_processed = sum(fog.tasks_processed for fog in simulation.fog_nodes)
    
    print(f"   Task Generation Rate: {total_tasks_generated / simulation.simulation_time:.2f} tasks/second")
    print(f"   Task Transmission Success Rate: {(total_tasks_sent / total_tasks_generated * 100):.1f}%")
    print(f"   Task Processing Success Rate: {(total_tasks_processed / total_tasks_sent * 100):.1f}%" if total_tasks_sent > 0 else "   Task Processing Success Rate: 0%")
    
    # Analyze IoT device performance
    print(f"\n   IoT Device Performance:")
    for i, device in enumerate(simulation.iot_devices, 1):
        success_rate = (device.tasks_sent / device.tasks_generated * 100) if device.tasks_generated > 0 else 0
        print(f"      Device {i} ({device.device_id}): {device.tasks_generated} generated, {device.tasks_sent} sent ({success_rate:.1f}% success)")
    
    # Analyze fog node performance
    print(f"\n   Fog Node Performance:")
    for i, fog_node in enumerate(simulation.fog_nodes, 1):
        stats = fog_node.get_task_statistics()
        print(f"      Fog Node {i} ({fog_node.node_id}): {stats['tasks_processed']} processed, {stats['utilization']:.1%} utilization")
    
    print("✅ Network performance analysis completed!\n")


def main():
    """Run all task processing examples."""
    print("🌐 Fog Computing Task Processing Examples")
    print("=" * 60)
    print("Demonstrating task generation and processing capabilities...\n")
    
    try:
        example_basic_task_processing()
        example_high_load_simulation()
        example_resource_utilization()
        example_task_complexity_analysis()
        example_network_performance()
        
        print("🎉 All task processing examples completed successfully!")
        print("The fog computing simulation now supports dynamic task generation and processing.")
        
    except Exception as e:
        print(f"❌ Example failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
