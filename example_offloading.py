"""
Example: Dynamic Task Offloading Engine
=====================================

This script demonstrates the intelligent task offloading capabilities
of the fog computing simulation environment.
"""

from fog_simulation import FogComputingSimulation


def example_basic_offloading():
    """Example: Basic offloading simulation."""
    print("📋 Example 1: Basic Offloading Simulation")
    print("-" * 40)
    
    # Create simulation with moderate duration
    simulation = FogComputingSimulation(simulation_time=30.0)
    simulation.setup_simulation(num_fog_nodes=2, num_iot_devices=8)
    
    # Run simulation
    simulation.run_simulation()
    
    # Print results
    simulation.print_simulation_results()
    print("✅ Basic offloading simulation completed!\n")


def example_high_load_offloading():
    """Example: High load scenario with increased offloading."""
    print("📋 Example 2: High Load Offloading Simulation")
    print("-" * 40)
    
    # Create simulation with many devices to increase load
    simulation = FogComputingSimulation(simulation_time=40.0)
    simulation.setup_simulation(num_fog_nodes=3, num_iot_devices=15)
    
    # Run simulation
    simulation.run_simulation()
    
    # Print results
    simulation.print_simulation_results()
    print("✅ High load offloading simulation completed!\n")


def example_offloading_analysis():
    """Example: Detailed offloading analysis."""
    print("📋 Example 3: Offloading Decision Analysis")
    print("-" * 40)
    
    # Create simulation
    simulation = FogComputingSimulation(simulation_time=25.0)
    simulation.setup_simulation(num_fog_nodes=2, num_iot_devices=10)
    
    # Run simulation
    simulation.run_simulation()
    
    # Detailed offloading analysis
    print("\n🔍 Detailed Offloading Analysis:")
    
    # Analyze fog node decisions
    for i, fog_node in enumerate(simulation.fog_nodes, 1):
        print(f"\n   Fog Node {i} ({fog_node.node_id}) Decision Analysis:")
        print(f"      Complexity threshold: {fog_node.complexity_threshold:.0f} MIPS")
        print(f"      Utilization threshold: {fog_node.utilization_threshold:.1%}")
        print(f"      Deadline threshold: {fog_node.deadline_threshold:.1f}s")
        print(f"      Cloud latency: {fog_node.cloud_latency:.1f}s")
        
        # Analyze task decisions
        local_tasks = [task for task in fog_node.pending_tasks 
                      if task.offload_decision and task.offload_decision.value == "process_locally"]
        offloaded_tasks = [task for task in fog_node.pending_tasks 
                          if task.offload_decision and task.offload_decision.value == "offload_to_cloud"]
        
        print(f"      Tasks processed locally: {len(local_tasks)}")
        print(f"      Tasks offloaded to cloud: {len(offloaded_tasks)}")
        
        if local_tasks:
            avg_complexity_local = sum(task.complexity_mips for task in local_tasks) / len(local_tasks)
            print(f"      Average complexity (local): {avg_complexity_local:.1f} MIPS")
        
        if offloaded_tasks:
            avg_complexity_offloaded = sum(task.complexity_mips for task in offloaded_tasks) / len(offloaded_tasks)
            print(f"      Average complexity (offloaded): {avg_complexity_offloaded:.1f} MIPS")
    
    # Cloud server analysis
    cloud_stats = simulation.cloud_server.get_task_statistics()
    print(f"\n   Cloud Server Analysis:")
    print(f"      Tasks received: {cloud_stats['tasks_processed']}")
    print(f"      Average processing time: {cloud_stats['average_processing_time']:.3f}s")
    print(f"      Resource utilization: {cloud_stats['utilization']:.1%}")
    
    print("✅ Offloading analysis completed!\n")


def example_decision_factors():
    """Example: Analyze decision factors and their impact."""
    print("📋 Example 4: Decision Factors Impact Analysis")
    print("-" * 40)
    
    # Create simulation
    simulation = FogComputingSimulation(simulation_time=20.0)
    simulation.setup_simulation(num_fog_nodes=1, num_iot_devices=6)
    
    # Run simulation
    simulation.run_simulation()
    
    # Analyze decision factors
    print("\n📊 Decision Factors Impact Analysis:")
    
    fog_node = simulation.fog_nodes[0]
    all_tasks = fog_node.pending_tasks
    
    if all_tasks:
        # Analyze by complexity
        high_complexity_tasks = [task for task in all_tasks if task.complexity_mips > fog_node.complexity_threshold]
        low_complexity_tasks = [task for task in all_tasks if task.complexity_mips <= fog_node.complexity_threshold]
        
        print(f"\n   Complexity Analysis:")
        print(f"      High complexity tasks (> {fog_node.complexity_threshold} MIPS): {len(high_complexity_tasks)}")
        print(f"      Low complexity tasks (≤ {fog_node.complexity_threshold} MIPS): {len(low_complexity_tasks)}")
        
        if high_complexity_tasks:
            offloaded_high = [task for task in high_complexity_tasks 
                            if task.offload_decision and task.offload_decision.value == "offload_to_cloud"]
            print(f"      High complexity offloading rate: {len(offloaded_high) / len(high_complexity_tasks) * 100:.1f}%")
        
        # Analyze by deadline
        tight_deadline_tasks = [task for task in all_tasks 
                              if (task.deadline - task.creation_time) < fog_node.deadline_threshold]
        normal_deadline_tasks = [task for task in all_tasks 
                               if (task.deadline - task.creation_time) >= fog_node.deadline_threshold]
        
        print(f"\n   Deadline Analysis:")
        print(f"      Tight deadline tasks (< {fog_node.deadline_threshold}s): {len(tight_deadline_tasks)}")
        print(f"      Normal deadline tasks (≥ {fog_node.deadline_threshold}s): {len(normal_deadline_tasks)}")
        
        if tight_deadline_tasks:
            offloaded_tight = [task for task in tight_deadline_tasks 
                             if task.offload_decision and task.offload_decision.value == "offload_to_cloud"]
            print(f"      Tight deadline offloading rate: {len(offloaded_tight) / len(tight_deadline_tasks) * 100:.1f}%")
        
        # Analyze offloading reasons
        offloaded_tasks = [task for task in all_tasks 
                          if task.offload_decision and task.offload_decision.value == "offload_to_cloud"]
        
        if offloaded_tasks:
            print(f"\n   Offloading Reasons:")
            reason_counts = {}
            for task in offloaded_tasks:
                if task.offload_reason:
                    # Extract main reason from the reason string
                    if "High complexity" in task.offload_reason:
                        reason_counts["High complexity"] = reason_counts.get("High complexity", 0) + 1
                    if "High CPU utilization" in task.offload_reason:
                        reason_counts["High CPU utilization"] = reason_counts.get("High CPU utilization", 0) + 1
                    if "Tight deadline" in task.offload_reason:
                        reason_counts["Tight deadline"] = reason_counts.get("Tight deadline", 0) + 1
                    if "Long queue" in task.offload_reason:
                        reason_counts["Long queue"] = reason_counts.get("Long queue", 0) + 1
            
            for reason, count in reason_counts.items():
                percentage = (count / len(offloaded_tasks)) * 100
                print(f"      {reason}: {count} tasks ({percentage:.1f}%)")
    
    print("✅ Decision factors analysis completed!\n")


def example_performance_comparison():
    """Example: Compare performance with and without offloading."""
    print("📋 Example 5: Performance Comparison")
    print("-" * 40)
    
    # Create simulation with offloading
    simulation = FogComputingSimulation(simulation_time=25.0)
    simulation.setup_simulation(num_fog_nodes=2, num_iot_devices=8)
    
    # Run simulation
    simulation.run_simulation()
    
    # Analyze performance metrics
    print("\n📈 Performance Metrics:")
    
    # Calculate offloading rate
    total_fog_processed = sum(fog.tasks_processed for fog in simulation.fog_nodes)
    total_fog_offloaded = sum(fog.tasks_offloaded for fog in simulation.fog_nodes)
    total_cloud_processed = simulation.cloud_server.tasks_processed
    
    offloading_rate = (total_fog_offloaded / (total_fog_processed + total_fog_offloaded) * 100) if (total_fog_processed + total_fog_offloaded) > 0 else 0
    
    print(f"   Offloading rate: {offloading_rate:.1f}%")
    print(f"   Local processing: {total_fog_processed} tasks")
    print(f"   Cloud processing: {total_cloud_processed} tasks")
    print(f"   Total processing: {total_fog_processed + total_cloud_processed} tasks")
    
    # Analyze resource utilization
    print(f"\n   Resource Utilization:")
    for i, fog_node in enumerate(simulation.fog_nodes, 1):
        stats = fog_node.get_task_statistics()
        print(f"      Fog Node {i}: {stats['utilization']:.1%}")
    
    cloud_stats = simulation.cloud_server.get_task_statistics()
    print(f"      Cloud Server: {cloud_stats['utilization']:.1%}")
    
    # Analyze processing times
    print(f"\n   Processing Times:")
    for i, fog_node in enumerate(simulation.fog_nodes, 1):
        stats = fog_node.get_task_statistics()
        print(f"      Fog Node {i} avg: {stats['average_processing_time']:.3f}s")
    
    print(f"      Cloud Server avg: {cloud_stats['average_processing_time']:.3f}s")
    
    print("✅ Performance comparison completed!\n")


def main():
    """Run all offloading examples."""
    print("🌐 Dynamic Task Offloading Engine Examples")
    print("=" * 60)
    print("Demonstrating intelligent task offloading capabilities...\n")
    
    try:
        example_basic_offloading()
        example_high_load_offloading()
        example_offloading_analysis()
        example_decision_factors()
        example_performance_comparison()
        
        print("🎉 All offloading examples completed successfully!")
        print("The dynamic task offloading engine is working effectively!")
        
    except Exception as e:
        print(f"❌ Example failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
