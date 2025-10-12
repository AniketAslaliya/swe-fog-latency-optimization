"""
Test Comparative Analysis
========================

A simplified test version of the comparative analysis to demonstrate
the functionality without running full simulations.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from typing import Dict, List, Tuple, Any
import json
from datetime import datetime


def create_sample_data():
    """Create sample data for testing the comparative analysis."""
    print("📊 Creating Sample Data for Comparative Analysis...")
    
    # Sample fog architecture data
    fog_data = {
        'task_events': [
            {'event_type': 'creation_time', 'task_id': 'FOG_TASK_001', 'timestamp': 1.0, 'task_complexity': 500, 'processing_location': 'IOT_001'},
            {'event_type': 'arrival_at_fog_time', 'task_id': 'FOG_TASK_001', 'timestamp': 1.1, 'task_complexity': 500, 'processing_location': 'FOG_001'},
            {'event_type': 'decision_time', 'task_id': 'FOG_TASK_001', 'timestamp': 1.2, 'task_complexity': 500, 'decision_made': 'process_locally', 'processing_location': 'FOG_001'},
            {'event_type': 'processing_start_time', 'task_id': 'FOG_TASK_001', 'timestamp': 1.3, 'task_complexity': 500, 'decision_made': 'process_locally', 'processing_location': 'FOG_001'},
            {'event_type': 'processing_end_time', 'task_id': 'FOG_TASK_001', 'timestamp': 1.8, 'task_complexity': 500, 'decision_made': 'process_locally', 'processing_location': 'FOG_001'},
            
            {'event_type': 'creation_time', 'task_id': 'FOG_TASK_002', 'timestamp': 2.0, 'task_complexity': 1500, 'processing_location': 'IOT_002'},
            {'event_type': 'arrival_at_fog_time', 'task_id': 'FOG_TASK_002', 'timestamp': 2.1, 'task_complexity': 1500, 'processing_location': 'FOG_001'},
            {'event_type': 'decision_time', 'task_id': 'FOG_TASK_002', 'timestamp': 2.2, 'task_complexity': 1500, 'decision_made': 'offload_to_cloud', 'processing_location': 'FOG_001'},
            {'event_type': 'arrival_at_cloud_time', 'task_id': 'FOG_TASK_002', 'timestamp': 2.5, 'task_complexity': 1500, 'decision_made': 'offload_to_cloud', 'processing_location': 'CLOUD_001'},
            {'event_type': 'processing_start_time', 'task_id': 'FOG_TASK_002', 'timestamp': 2.6, 'task_complexity': 1500, 'decision_made': 'offload_to_cloud', 'processing_location': 'CLOUD_001'},
            {'event_type': 'processing_end_time', 'task_id': 'FOG_TASK_002', 'timestamp': 2.8, 'task_complexity': 1500, 'decision_made': 'offload_to_cloud', 'processing_location': 'CLOUD_001'},
            
            {'event_type': 'creation_time', 'task_id': 'FOG_TASK_003', 'timestamp': 3.0, 'task_complexity': 800, 'processing_location': 'IOT_003'},
            {'event_type': 'arrival_at_fog_time', 'task_id': 'FOG_TASK_003', 'timestamp': 3.1, 'task_complexity': 800, 'processing_location': 'FOG_002'},
            {'event_type': 'decision_time', 'task_id': 'FOG_TASK_003', 'timestamp': 3.2, 'task_complexity': 800, 'decision_made': 'process_locally', 'processing_location': 'FOG_002'},
            {'event_type': 'processing_start_time', 'task_id': 'FOG_TASK_003', 'timestamp': 3.3, 'task_complexity': 800, 'decision_made': 'process_locally', 'processing_location': 'FOG_002'},
            {'event_type': 'processing_end_time', 'task_id': 'FOG_TASK_003', 'timestamp': 3.9, 'task_complexity': 800, 'decision_made': 'process_locally', 'processing_location': 'FOG_002'},
        ],
        'resource_monitoring': [],
        'performance_summary': {
            'total_events': 15,
            'total_tasks': 3,
            'average_response_time': 0.6,
            'average_processing_time': 0.5,
            'average_decision_time': 0.1,
            'resource_monitoring_entries': 0
        }
    }
    
    # Sample cloud-only data
    cloud_only_data = {
        'task_events': [
            {'event_type': 'creation_time', 'task_id': 'CLOUD_TASK_001', 'timestamp': 1.0, 'task_complexity': 500, 'processing_location': 'CLOUD_IOT_001'},
            {'event_type': 'arrival_at_cloud_time', 'task_id': 'CLOUD_TASK_001', 'timestamp': 1.3, 'task_complexity': 500, 'processing_location': 'CLOUD_001'},
            {'event_type': 'processing_start_time', 'task_id': 'CLOUD_TASK_001', 'timestamp': 1.4, 'task_complexity': 500, 'processing_location': 'CLOUD_001'},
            {'event_type': 'processing_end_time', 'task_id': 'CLOUD_TASK_001', 'timestamp': 1.6, 'task_complexity': 500, 'processing_location': 'CLOUD_001'},
            
            {'event_type': 'creation_time', 'task_id': 'CLOUD_TASK_002', 'timestamp': 2.0, 'task_complexity': 1500, 'processing_location': 'CLOUD_IOT_002'},
            {'event_type': 'arrival_at_cloud_time', 'task_id': 'CLOUD_TASK_002', 'timestamp': 2.4, 'task_complexity': 1500, 'processing_location': 'CLOUD_001'},
            {'event_type': 'processing_start_time', 'task_id': 'CLOUD_TASK_002', 'timestamp': 2.5, 'task_complexity': 1500, 'processing_location': 'CLOUD_001'},
            {'event_type': 'processing_end_time', 'task_id': 'CLOUD_TASK_002', 'timestamp': 2.7, 'task_complexity': 1500, 'processing_location': 'CLOUD_001'},
            
            {'event_type': 'creation_time', 'task_id': 'CLOUD_TASK_003', 'timestamp': 3.0, 'task_complexity': 800, 'processing_location': 'CLOUD_IOT_003'},
            {'event_type': 'arrival_at_cloud_time', 'task_id': 'CLOUD_TASK_003', 'timestamp': 3.3, 'task_complexity': 800, 'processing_location': 'CLOUD_001'},
            {'event_type': 'processing_start_time', 'task_id': 'CLOUD_TASK_003', 'timestamp': 3.4, 'task_complexity': 800, 'processing_location': 'CLOUD_001'},
            {'event_type': 'processing_end_time', 'task_id': 'CLOUD_TASK_003', 'timestamp': 3.6, 'task_complexity': 800, 'processing_location': 'CLOUD_001'},
        ],
        'resource_monitoring': [],
        'performance_summary': {
            'total_events': 12,
            'total_tasks': 3,
            'average_response_time': 0.6,
            'average_processing_time': 0.2,
            'average_decision_time': 0.0,
            'resource_monitoring_entries': 0
        }
    }
    
    return fog_data, cloud_only_data


def create_dataframes(fog_data, cloud_only_data):
    """Convert sample data to Pandas DataFrames."""
    print("📊 Creating DataFrames...")
    
    # Create Fog Architecture DataFrame
    fog_events = fog_data['task_events']
    fog_df = pd.DataFrame(fog_events)
    
    # Create Cloud-Only DataFrame
    cloud_events = cloud_only_data['task_events']
    cloud_only_df = pd.DataFrame(cloud_events)
    
    # Calculate end-to-end latency for both architectures
    fog_df = calculate_latency_metrics(fog_df, 'fog')
    cloud_only_df = calculate_latency_metrics(cloud_only_df, 'cloud_only')
    
    print(f"   ✓ Fog Architecture DataFrame: {len(fog_df)} events")
    print(f"   ✓ Cloud-Only DataFrame: {len(cloud_only_df)} events")
    
    return fog_df, cloud_only_df


def calculate_latency_metrics(df: pd.DataFrame, architecture: str) -> pd.DataFrame:
    """Calculate latency metrics for a given architecture."""
    task_metrics = []
    
    for task_id in df['task_id'].unique():
        task_events = df[df['task_id'] == task_id].sort_values('timestamp')
        
        # Extract key timestamps
        creation_time = task_events[task_events['event_type'] == 'creation_time']['timestamp'].iloc[0] if len(task_events[task_events['event_type'] == 'creation_time']) > 0 else None
        processing_end_time = task_events[task_events['event_type'] == 'processing_end_time']['timestamp'].iloc[0] if len(task_events[task_events['event_type'] == 'processing_end_time']) > 0 else None
        
        if creation_time is not None and processing_end_time is not None:
            end_to_end_latency = processing_end_time - creation_time
            
            # Get task complexity
            complexity = task_events['task_complexity'].iloc[0] if 'task_complexity' in task_events.columns else None
            
            # Get processing location
            processing_location = task_events[task_events['event_type'] == 'processing_start_time']['processing_location'].iloc[0] if len(task_events[task_events['event_type'] == 'processing_start_time']) > 0 else 'unknown'
            
            # Get decision made
            decision_made = task_events[task_events['event_type'] == 'decision_time']['decision_made'].iloc[0] if len(task_events[task_events['event_type'] == 'decision_time']) > 0 else 'cloud_only'
            
            task_metrics.append({
                'task_id': task_id,
                'architecture': architecture,
                'end_to_end_latency': end_to_end_latency,
                'task_complexity': complexity,
                'processing_location': processing_location,
                'decision_made': decision_made,
                'creation_time': creation_time,
                'processing_end_time': processing_end_time
            })
    
    return pd.DataFrame(task_metrics)


def calculate_performance_metrics(fog_df, cloud_only_df):
    """Calculate comprehensive performance metrics."""
    print("\n📈 Calculating Performance Metrics...")
    
    metrics = {}
    
    # Fog Architecture Metrics
    if fog_df is not None and not fog_df.empty:
        fog_metrics = {
            'average_latency': fog_df['end_to_end_latency'].mean(),
            'median_latency': fog_df['end_to_end_latency'].median(),
            'std_latency': fog_df['end_to_end_latency'].std(),
            'min_latency': fog_df['end_to_end_latency'].min(),
            'max_latency': fog_df['end_to_end_latency'].max(),
            'total_tasks': len(fog_df),
            'fog_processed': len(fog_df[fog_df['processing_location'].str.contains('FOG', na=False)]),
            'cloud_processed': len(fog_df[fog_df['processing_location'].str.contains('CLOUD', na=False)]),
            'offload_rate': len(fog_df[fog_df['decision_made'] == 'offload_to_cloud']) / len(fog_df) * 100 if len(fog_df) > 0 else 0
        }
        metrics['fog'] = fog_metrics
    
    # Cloud-Only Architecture Metrics
    if cloud_only_df is not None and not cloud_only_df.empty:
        cloud_metrics = {
            'average_latency': cloud_only_df['end_to_end_latency'].mean(),
            'median_latency': cloud_only_df['end_to_end_latency'].median(),
            'std_latency': cloud_only_df['end_to_end_latency'].std(),
            'min_latency': cloud_only_df['end_to_end_latency'].min(),
            'max_latency': cloud_only_df['end_to_end_latency'].max(),
            'total_tasks': len(cloud_only_df),
            'cloud_processed': len(cloud_only_df),
            'offload_rate': 100.0  # All tasks go to cloud
        }
        metrics['cloud_only'] = cloud_metrics
    
    # Print metrics
    print("\n📊 Performance Comparison Results:")
    print("=" * 50)
    
    if 'fog' in metrics:
        print(f"\n🌫️  Fog Architecture:")
        print(f"   Average Latency: {metrics['fog']['average_latency']:.3f}s")
        print(f"   Median Latency: {metrics['fog']['median_latency']:.3f}s")
        print(f"   Tasks Processed Locally: {metrics['fog']['fog_processed']}")
        print(f"   Tasks Offloaded to Cloud: {metrics['fog']['cloud_processed']}")
        print(f"   Offloading Rate: {metrics['fog']['offload_rate']:.1f}%")
    
    if 'cloud_only' in metrics:
        print(f"\n☁️  Cloud-Only Architecture:")
        print(f"   Average Latency: {metrics['cloud_only']['average_latency']:.3f}s")
        print(f"   Median Latency: {metrics['cloud_only']['median_latency']:.3f}s")
        print(f"   All Tasks to Cloud: {metrics['cloud_only']['cloud_processed']}")
        print(f"   Offloading Rate: {metrics['cloud_only']['offload_rate']:.1f}%")
    
    # Calculate improvement
    if 'fog' in metrics and 'cloud_only' in metrics:
        latency_improvement = ((metrics['cloud_only']['average_latency'] - metrics['fog']['average_latency']) / metrics['cloud_only']['average_latency']) * 100
        print(f"\n🎯 Performance Improvement:")
        print(f"   Latency Reduction: {latency_improvement:.1f}%")
        print(f"   Fog is {'better' if latency_improvement > 0 else 'worse'} than Cloud-Only")
    
    return metrics


def create_visualizations(fog_df, cloud_only_df, metrics):
    """Create comprehensive visualizations."""
    print("\n📊 Creating Comparative Visualizations...")
    
    # Set up the plotting style
    plt.style.use('default')
    sns.set_palette("husl")
    
    # Create figure with subplots
    fig = plt.figure(figsize=(20, 15))
    
    # 1. Bar Chart: Average End-to-End Latency Comparison
    ax1 = plt.subplot(2, 3, 1)
    create_latency_comparison_bar_chart(ax1, metrics)
    
    # 2. Scatter Plot: End-to-End Latency vs Task Complexity
    ax2 = plt.subplot(2, 3, 2)
    create_latency_complexity_scatter(ax2, fog_df, cloud_only_df)
    
    # 3. Box Plot: Latency Distribution Comparison
    ax3 = plt.subplot(2, 3, 3)
    create_latency_distribution_boxplot(ax3, fog_df, cloud_only_df)
    
    # 4. Processing Location Distribution
    ax4 = plt.subplot(2, 3, 4)
    create_processing_location_chart(ax4, fog_df)
    
    # 5. Latency vs Time
    ax5 = plt.subplot(2, 3, 5)
    create_latency_timeline(ax5, fog_df, cloud_only_df)
    
    # 6. Performance Metrics Summary
    ax6 = plt.subplot(2, 3, 6)
    create_metrics_summary_table(ax6, metrics)
    
    plt.tight_layout()
    
    # Save plot
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"comparative_analysis_demo_{timestamp}.png"
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"   ✓ Plots saved to: {filename}")
    
    plt.show()
    print("✅ Visualizations created successfully!")


def create_latency_comparison_bar_chart(ax, metrics):
    """Create bar chart comparing average latencies."""
    if metrics:
        architectures = []
        latencies = []
        
        if 'fog' in metrics:
            architectures.append('Fog Architecture')
            latencies.append(metrics['fog']['average_latency'])
        
        if 'cloud_only' in metrics:
            architectures.append('Cloud-Only')
            latencies.append(metrics['cloud_only']['average_latency'])
        
        bars = ax.bar(architectures, latencies, color=['#2E8B57', '#FF6347'], alpha=0.8)
        ax.set_title('Average End-to-End Latency Comparison', fontsize=14, fontweight='bold')
        ax.set_ylabel('Average Latency (seconds)', fontsize=12)
        ax.set_xlabel('Architecture', fontsize=12)
        
        # Add value labels on bars
        for bar, latency in zip(bars, latencies):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.001,
                   f'{latency:.3f}s', ha='center', va='bottom', fontweight='bold')
        
        # Add improvement percentage if both architectures exist
        if len(latencies) == 2:
            improvement = ((latencies[1] - latencies[0]) / latencies[1]) * 100
            ax.text(0.5, max(latencies) * 0.8, f'Improvement: {improvement:.1f}%', 
                   ha='center', va='center', fontsize=12, fontweight='bold',
                   bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7))


def create_latency_complexity_scatter(ax, fog_df, cloud_only_df):
    """Create scatter plot of latency vs complexity."""
    if fog_df is not None and not fog_df.empty:
        # Plot fog data
        fog_data = fog_df[fog_df['architecture'] == 'fog']
        if not fog_data.empty:
            # Color by processing location
            fog_colors = ['#2E8B57' if 'FOG' in str(loc) else '#FF6347' for loc in fog_data['processing_location']]
            ax.scatter(fog_data['task_complexity'], fog_data['end_to_end_latency'], 
                      c=fog_colors, alpha=0.6, s=50, label='Fog Architecture', edgecolors='black', linewidth=0.5)
    
    if cloud_only_df is not None and not cloud_only_df.empty:
        # Plot cloud-only data
        ax.scatter(cloud_only_df['task_complexity'], cloud_only_df['end_to_end_latency'], 
                  c='#FF6347', alpha=0.6, s=50, label='Cloud-Only', marker='s', edgecolors='black', linewidth=0.5)
    
    ax.set_title('End-to-End Latency vs Task Complexity', fontsize=14, fontweight='bold')
    ax.set_xlabel('Task Complexity (MIPS)', fontsize=12)
    ax.set_ylabel('End-to-End Latency (seconds)', fontsize=12)
    ax.legend()
    ax.grid(True, alpha=0.3)


def create_latency_distribution_boxplot(ax, fog_df, cloud_only_df):
    """Create box plot comparing latency distributions."""
    data_to_plot = []
    labels = []
    
    if fog_df is not None and not fog_df.empty:
        data_to_plot.append(fog_df['end_to_end_latency'].values)
        labels.append('Fog Architecture')
    
    if cloud_only_df is not None and not cloud_only_df.empty:
        data_to_plot.append(cloud_only_df['end_to_end_latency'].values)
        labels.append('Cloud-Only')
    
    if data_to_plot:
        box_plot = ax.boxplot(data_to_plot, labels=labels, patch_artist=True)
        colors = ['#2E8B57', '#FF6347']
        for patch, color in zip(box_plot['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)
        
        ax.set_title('Latency Distribution Comparison', fontsize=14, fontweight='bold')
        ax.set_ylabel('End-to-End Latency (seconds)', fontsize=12)
        ax.grid(True, alpha=0.3)


def create_processing_location_chart(ax, fog_df):
    """Create pie chart showing processing location distribution."""
    if fog_df is not None and not fog_df.empty:
        # Count processing locations
        location_counts = fog_df['processing_location'].value_counts()
        
        # Separate fog and cloud processing
        fog_count = sum(count for loc, count in location_counts.items() if 'FOG' in str(loc))
        cloud_count = sum(count for loc, count in location_counts.items() if 'CLOUD' in str(loc))
        
        sizes = [fog_count, cloud_count]
        labels = ['Fog Processing', 'Cloud Processing']
        colors = ['#2E8B57', '#FF6347']
        
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax.set_title('Fog Architecture Processing Distribution', fontsize=14, fontweight='bold')


def create_latency_timeline(ax, fog_df, cloud_only_df):
    """Create timeline showing latency over time."""
    if fog_df is not None and not fog_df.empty:
        # Sort by creation time
        timeline_data = fog_df.sort_values('creation_time')
        
        ax.plot(timeline_data['creation_time'], timeline_data['end_to_end_latency'], 
               'o-', color='#2E8B57', alpha=0.7, markersize=4, label='Fog Architecture')
    
    if cloud_only_df is not None and not cloud_only_df.empty:
        timeline_data = cloud_only_df.sort_values('creation_time')
        
        ax.plot(timeline_data['creation_time'], timeline_data['end_to_end_latency'], 
               's-', color='#FF6347', alpha=0.7, markersize=4, label='Cloud-Only')
    
    ax.set_title('Latency Timeline', fontsize=14, fontweight='bold')
    ax.set_xlabel('Simulation Time', fontsize=12)
    ax.set_ylabel('End-to-End Latency (seconds)', fontsize=12)
    ax.legend()
    ax.grid(True, alpha=0.3)


def create_metrics_summary_table(ax, metrics):
    """Create summary table of key metrics."""
    ax.axis('off')
    
    if metrics:
        # Create table data
        table_data = []
        
        if 'fog' in metrics:
            fog_metrics = metrics['fog']
            table_data.append(['Fog Architecture', f"{fog_metrics['average_latency']:.3f}s", 
                             f"{fog_metrics['offload_rate']:.1f}%", f"{fog_metrics['total_tasks']}"])
        
        if 'cloud_only' in metrics:
            cloud_metrics = metrics['cloud_only']
            table_data.append(['Cloud-Only', f"{cloud_metrics['average_latency']:.3f}s", 
                             f"{cloud_metrics['offload_rate']:.1f}%", f"{cloud_metrics['total_tasks']}"])
        
        # Create table
        table = ax.table(cellText=table_data,
                       colLabels=['Architecture', 'Avg Latency', 'Offload Rate', 'Total Tasks'],
                       cellLoc='center',
                       loc='center',
                       bbox=[0, 0, 1, 1])
        
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 2)
        
        # Style the table
        for i in range(len(table_data) + 1):
            for j in range(4):
                cell = table[(i, j)]
                if i == 0:  # Header
                    cell.set_facecolor('#4CAF50')
                    cell.set_text_props(weight='bold', color='white')
                else:
                    cell.set_facecolor('#F0F0F0' if i % 2 == 0 else 'white')
        
        ax.set_title('Performance Metrics Summary', fontsize=14, fontweight='bold', pad=20)


def main():
    """Main function to run test comparative analysis."""
    print("🚀 Running Test Comparative Analysis")
    print("=" * 60)
    
    # Step 1: Create sample data
    fog_data, cloud_only_data = create_sample_data()
    
    # Step 2: Create DataFrames
    fog_df, cloud_only_df = create_dataframes(fog_data, cloud_only_data)
    
    # Step 3: Calculate metrics
    metrics = calculate_performance_metrics(fog_df, cloud_only_df)
    
    # Step 4: Create visualizations
    create_visualizations(fog_df, cloud_only_df, metrics)
    
    print("\n🎉 Test Comparative Analysis Completed!")
    print("✅ All analysis steps completed successfully!")


if __name__ == "__main__":
    main()
