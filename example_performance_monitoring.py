"""
Example: Performance Monitoring and Data Logging
===============================================

This script demonstrates the comprehensive performance monitoring and data logging
capabilities of the fog computing simulation environment.
"""

from fog_simulation import FogComputingSimulation, global_logger
import json


def example_basic_monitoring():
    """Example: Basic performance monitoring."""
    print("📋 Example 1: Basic Performance Monitoring")
    print("-" * 40)
    
    # Create simulation with monitoring
    simulation = FogComputingSimulation(simulation_time=10.0)
    simulation.setup_simulation(num_fog_nodes=2, num_iot_devices=5)
    
    # Run simulation
    simulation.run_simulation()
    
    # Get performance summary
    summary = global_logger.get_performance_summary()
    print(f"\n📊 Performance Summary:")
    print(f"   Total events logged: {summary.get('total_events', 0)}")
    print(f"   Total tasks tracked: {summary.get('total_tasks', 0)}")
    print(f"   Average response time: {summary.get('average_response_time', 0):.3f}s")
    print(f"   Average processing time: {summary.get('average_processing_time', 0):.3f}s")
    print(f"   Average decision time: {summary.get('average_decision_time', 0):.3f}s")
    print(f"   Resource monitoring entries: {summary.get('resource_monitoring_entries', 0)}")
    
    print("✅ Basic monitoring example completed!\n")


def example_task_lifecycle_analysis():
    """Example: Detailed task lifecycle analysis."""
    print("📋 Example 2: Task Lifecycle Analysis")
    print("-" * 40)
    
    # Create simulation
    simulation = FogComputingSimulation(simulation_time=8.0)
    simulation.setup_simulation(num_fog_nodes=1, num_iot_devices=3)
    
    # Run simulation
    simulation.run_simulation()
    
    # Analyze task lifecycles
    task_events = global_logger.task_events
    
    if task_events:
        # Get unique task IDs
        task_ids = list(set(event['task_id'] for event in task_events))
        print(f"\n🔍 Task Lifecycle Analysis:")
        print(f"   Total unique tasks: {len(task_ids)}")
        
        # Analyze first few tasks in detail
        for i, task_id in enumerate(task_ids[:3]):  # Analyze first 3 tasks
            lifecycle = global_logger.get_task_lifecycle(task_id)
            print(f"\n   Task {i+1} ({task_id}):")
            
            # Sort events by timestamp
            lifecycle.sort(key=lambda x: x['timestamp'])
            
            for event in lifecycle:
                print(f"      {event['event_type']}: {event['timestamp']:.3f}s")
                if event.get('decision_made'):
                    print(f"         Decision: {event['decision_made']}")
                if event.get('processing_location'):
                    print(f"         Location: {event['processing_location']}")
        
        # Calculate lifecycle metrics
        creation_events = [e for e in task_events if e['event_type'] == 'creation_time']
        completion_events = [e for e in task_events if e['event_type'] == 'processing_end_time']
        
        if creation_events and completion_events:
            print(f"\n   Lifecycle Metrics:")
            print(f"      Tasks created: {len(creation_events)}")
            print(f"      Tasks completed: {len(completion_events)}")
            print(f"      Completion rate: {len(completion_events)/len(creation_events)*100:.1f}%")
    
    print("✅ Task lifecycle analysis completed!\n")


def example_resource_utilization_analysis():
    """Example: Resource utilization analysis."""
    print("📋 Example 3: Resource Utilization Analysis")
    print("-" * 40)
    
    # Create simulation
    simulation = FogComputingSimulation(simulation_time=12.0)
    simulation.setup_simulation(num_fog_nodes=3, num_iot_devices=8)
    
    # Run simulation
    simulation.run_simulation()
    
    # Analyze resource utilization
    resource_data = global_logger.resource_monitoring
    
    if resource_data:
        print(f"\n📈 Resource Utilization Analysis:")
        print(f"   Total monitoring entries: {len(resource_data)}")
        
        # Group by node type
        fog_data = [r for r in resource_data if r['node_type'] == 'fog']
        cloud_data = [r for r in resource_data if r['node_type'] == 'cloud']
        
        print(f"   Fog node entries: {len(fog_data)}")
        print(f"   Cloud server entries: {len(cloud_data)}")
        
        # Calculate average utilization
        if fog_data:
            avg_fog_utilization = sum(r['utilization'] for r in fog_data) / len(fog_data)
            max_fog_utilization = max(r['utilization'] for r in fog_data)
            print(f"   Average fog utilization: {avg_fog_utilization:.1%}")
            print(f"   Peak fog utilization: {max_fog_utilization:.1%}")
        
        if cloud_data:
            avg_cloud_utilization = sum(r['utilization'] for r in cloud_data) / len(cloud_data)
            max_cloud_utilization = max(r['utilization'] for r in cloud_data)
            print(f"   Average cloud utilization: {avg_cloud_utilization:.1%}")
            print(f"   Peak cloud utilization: {max_cloud_utilization:.1%}")
        
        # Analyze queue lengths
        if fog_data:
            avg_queue_length = sum(r['queue_length'] for r in fog_data) / len(fog_data)
            max_queue_length = max(r['queue_length'] for r in fog_data)
            print(f"   Average fog queue length: {avg_queue_length:.1f}")
            print(f"   Peak fog queue length: {max_queue_length}")
    
    print("✅ Resource utilization analysis completed!\n")


def example_decision_pattern_analysis():
    """Example: Decision pattern analysis."""
    print("📋 Example 4: Decision Pattern Analysis")
    print("-" * 40)
    
    # Create simulation
    simulation = FogComputingSimulation(simulation_time=15.0)
    simulation.setup_simulation(num_fog_nodes=2, num_iot_devices=6)
    
    # Run simulation
    simulation.run_simulation()
    
    # Analyze decision patterns
    task_events = global_logger.task_events
    decision_events = [e for e in task_events if e['event_type'] == 'decision_time']
    
    if decision_events:
        print(f"\n🧠 Decision Pattern Analysis:")
        print(f"   Total decisions made: {len(decision_events)}")
        
        # Analyze decision types
        decisions = [e['decision_made'] for e in decision_events if e['decision_made']]
        decision_counts = {}
        for decision in decisions:
            decision_counts[decision] = decision_counts.get(decision, 0) + 1
        
        print(f"   Decision distribution:")
        for decision, count in decision_counts.items():
            percentage = (count / len(decisions)) * 100
            print(f"      {decision}: {count} ({percentage:.1f}%)")
        
        # Analyze decision reasons
        print(f"\n   Decision Reasons:")
        for event in decision_events[:5]:  # Show first 5 decisions
            if event.get('additional_data', {}).get('reason'):
                reason = event['additional_data']['reason']
                print(f"      {event['task_id']}: {reason}")
        
        # Analyze complexity vs decision
        local_decisions = [e for e in decision_events if e['decision_made'] == 'process_locally']
        offload_decisions = [e for e in decision_events if e['decision_made'] == 'offload_to_cloud']
        
        if local_decisions:
            avg_local_complexity = sum(e['task_complexity'] for e in local_decisions if e['task_complexity']) / len(local_decisions)
            print(f"   Average complexity (local): {avg_local_complexity:.1f} MIPS")
        
        if offload_decisions:
            avg_offload_complexity = sum(e['task_complexity'] for e in offload_decisions if e['task_complexity']) / len(offload_decisions)
            print(f"   Average complexity (offloaded): {avg_offload_complexity:.1f} MIPS")
    
    print("✅ Decision pattern analysis completed!\n")


def example_data_export_and_analysis():
    """Example: Data export and external analysis."""
    print("📋 Example 5: Data Export and Analysis")
    print("-" * 40)
    
    # Create simulation
    simulation = FogComputingSimulation(simulation_time=10.0)
    simulation.setup_simulation(num_fog_nodes=2, num_iot_devices=4)
    
    # Run simulation
    simulation.run_simulation()
    
    # Export all data
    exported_data = global_logger.export_data()
    
    print(f"\n💾 Data Export:")
    print(f"   Task events: {len(exported_data['task_events'])}")
    print(f"   Resource monitoring: {len(exported_data['resource_monitoring'])}")
    print(f"   Performance summary: {len(exported_data['performance_summary'])} fields")
    
    # Save to file (optional)
    try:
        with open('simulation_data.json', 'w') as f:
            json.dump(exported_data, f, indent=2, default=str)
        print(f"   ✓ Data exported to simulation_data.json")
    except Exception as e:
        print(f"   ⚠️  Could not save to file: {e}")
    
    # Perform external analysis
    task_events = exported_data['task_events']
    
    # Calculate processing time distribution
    processing_events = [e for e in task_events if e['event_type'] == 'processing_start_time']
    completion_events = [e for e in task_events if e['event_type'] == 'processing_end_time']
    
    if processing_events and completion_events:
        processing_times = []
        for start_event in processing_events:
            task_id = start_event['task_id']
            end_events = [e for e in completion_events if e['task_id'] == task_id]
            if end_events:
                processing_time = end_events[0]['timestamp'] - start_event['timestamp']
                processing_times.append(processing_time)
        
        if processing_times:
            avg_processing = sum(processing_times) / len(processing_times)
            min_processing = min(processing_times)
            max_processing = max(processing_times)
            
            print(f"\n   Processing Time Analysis:")
            print(f"      Average: {avg_processing:.3f}s")
            print(f"      Minimum: {min_processing:.3f}s")
            print(f"      Maximum: {max_processing:.3f}s")
    
    print("✅ Data export and analysis completed!\n")


def main():
    """Run all performance monitoring examples."""
    print("🌐 Performance Monitoring and Data Logging Examples")
    print("=" * 60)
    print("Demonstrating comprehensive performance monitoring capabilities...\n")
    
    try:
        example_basic_monitoring()
        example_task_lifecycle_analysis()
        example_resource_utilization_analysis()
        example_decision_pattern_analysis()
        example_data_export_and_analysis()
        
        print("🎉 All performance monitoring examples completed successfully!")
        print("The comprehensive performance monitoring system is working effectively!")
        
    except Exception as e:
        print(f"❌ Example failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
