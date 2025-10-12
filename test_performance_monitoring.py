"""
Test script for Performance Monitoring and Data Logging
=====================================================

This script tests the comprehensive performance monitoring and data logging
functionality of the fog computing simulation environment.
"""

import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fog_simulation import (
    FogComputingSimulation, 
    global_logger,
    Task, 
    TaskStatus,
    OffloadDecision
)


def test_performance_logging():
    """Test the performance logging functionality."""
    print("🧪 Testing Performance Logging...")
    
    # Create a short simulation to test logging
    simulation = FogComputingSimulation(simulation_time=5.0)
    simulation.setup_simulation(num_fog_nodes=2, num_iot_devices=3)
    
    # Run simulation
    simulation.run_simulation()
    
    # Check if events were logged
    performance_summary = global_logger.get_performance_summary()
    assert performance_summary['total_events'] > 0, "No events were logged"
    assert performance_summary['total_tasks'] > 0, "No tasks were tracked"
    assert performance_summary['resource_monitoring_entries'] > 0, "No resource monitoring data"
    
    print(f"   ✓ Total events logged: {performance_summary['total_events']}")
    print(f"   ✓ Total tasks tracked: {performance_summary['total_tasks']}")
    print(f"   ✓ Resource monitoring entries: {performance_summary['resource_monitoring_entries']}")
    print("   ✅ Performance logging test passed!\n")


def test_task_lifecycle_tracking():
    """Test task lifecycle event tracking."""
    print("🧪 Testing Task Lifecycle Tracking...")
    
    # Get all task events
    task_events = global_logger.task_events
    
    # Check for different event types
    event_types = set(event['event_type'] for event in task_events)
    expected_events = {'creation_time', 'arrival_at_fog_time', 'decision_time', 
                      'processing_start_time', 'processing_end_time'}
    
    # Check if we have the expected event types
    found_events = expected_events.intersection(event_types)
    assert len(found_events) > 0, f"Expected event types not found. Found: {event_types}"
    
    print(f"   ✓ Event types found: {sorted(found_events)}")
    print(f"   ✓ Total event types: {len(event_types)}")
    
    # Test task lifecycle retrieval
    if task_events:
        sample_task_id = task_events[0]['task_id']
        lifecycle = global_logger.get_task_lifecycle(sample_task_id)
        assert len(lifecycle) > 0, "Task lifecycle not found"
        print(f"   ✓ Sample task lifecycle events: {len(lifecycle)}")
    
    print("   ✅ Task lifecycle tracking test passed!\n")


def test_resource_monitoring():
    """Test resource utilization monitoring."""
    print("🧪 Testing Resource Monitoring...")
    
    # Get resource monitoring data
    resource_data = global_logger.resource_monitoring
    
    assert len(resource_data) > 0, "No resource monitoring data found"
    
    # Check data structure
    sample_entry = resource_data[0]
    required_fields = ['timestamp', 'node_id', 'utilization', 'queue_length', 
                      'processing_capacity', 'node_type']
    
    for field in required_fields:
        assert field in sample_entry, f"Missing field: {field}"
    
    # Check node types
    node_types = set(entry['node_type'] for entry in resource_data)
    assert 'fog' in node_types or 'cloud' in node_types, "No fog or cloud monitoring data"
    
    print(f"   ✓ Resource monitoring entries: {len(resource_data)}")
    print(f"   ✓ Node types monitored: {sorted(node_types)}")
    print(f"   ✓ Sample utilization: {sample_entry['utilization']:.1%}")
    print("   ✅ Resource monitoring test passed!\n")


def test_performance_metrics():
    """Test performance metrics calculation."""
    print("🧪 Testing Performance Metrics...")
    
    # Get performance summary
    summary = global_logger.get_performance_summary()
    
    # Check if metrics are calculated
    assert 'average_response_time' in summary, "Average response time not calculated"
    assert 'average_processing_time' in summary, "Average processing time not calculated"
    assert 'average_decision_time' in summary, "Average decision time not calculated"
    
    print(f"   ✓ Average response time: {summary['average_response_time']:.3f}s")
    print(f"   ✓ Average processing time: {summary['average_processing_time']:.3f}s")
    print(f"   ✓ Average decision time: {summary['average_decision_time']:.3f}s")
    print("   ✅ Performance metrics test passed!\n")


def test_data_export():
    """Test data export functionality."""
    print("🧪 Testing Data Export...")
    
    # Export all data
    exported_data = global_logger.export_data()
    
    # Check export structure
    assert 'task_events' in exported_data, "Task events not in export"
    assert 'resource_monitoring' in exported_data, "Resource monitoring not in export"
    assert 'performance_summary' in exported_data, "Performance summary not in export"
    
    # Check data integrity
    assert len(exported_data['task_events']) > 0, "No task events in export"
    assert len(exported_data['resource_monitoring']) > 0, "No resource monitoring in export"
    assert exported_data['performance_summary']['total_events'] > 0, "No events in summary"
    
    print(f"   ✓ Exported task events: {len(exported_data['task_events'])}")
    print(f"   ✓ Exported resource data: {len(exported_data['resource_monitoring'])}")
    print(f"   ✓ Export structure complete")
    print("   ✅ Data export test passed!\n")


def test_detailed_analysis():
    """Test detailed performance analysis."""
    print("🧪 Testing Detailed Performance Analysis...")
    
    # Get task events for analysis
    task_events = global_logger.task_events
    
    if task_events:
        # Analyze event distribution
        event_counts = {}
        for event in task_events:
            event_type = event['event_type']
            event_counts[event_type] = event_counts.get(event_type, 0) + 1
        
        print(f"   ✓ Event distribution:")
        for event_type, count in sorted(event_counts.items()):
            print(f"      {event_type}: {count}")
        
        # Analyze decision patterns
        decision_events = [e for e in task_events if e['event_type'] == 'decision_time']
        if decision_events:
            decisions = [e['decision_made'] for e in decision_events if e['decision_made']]
            decision_counts = {}
            for decision in decisions:
                decision_counts[decision] = decision_counts.get(decision, 0) + 1
            
            print(f"   ✓ Decision patterns:")
            for decision, count in decision_counts.items():
                print(f"      {decision}: {count}")
        
        # Analyze processing locations
        processing_events = [e for e in task_events if e['event_type'] == 'processing_start_time']
        if processing_events:
            locations = [e['processing_location'] for e in processing_events if e['processing_location']]
            location_counts = {}
            for location in locations:
                location_counts[location] = location_counts.get(location, 0) + 1
            
            print(f"   ✓ Processing locations:")
            for location, count in location_counts.items():
                print(f"      {location}: {count}")
    
    print("   ✅ Detailed analysis test passed!\n")


def run_all_tests():
    """Run all performance monitoring tests."""
    print("🚀 Running Performance Monitoring and Data Logging Tests")
    print("=" * 70)
    
    try:
        test_performance_logging()
        test_task_lifecycle_tracking()
        test_resource_monitoring()
        test_performance_metrics()
        test_data_export()
        test_detailed_analysis()
        
        print("🎉 All performance monitoring tests passed successfully!")
        print("✅ Comprehensive performance monitoring and data logging is working correctly.")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
