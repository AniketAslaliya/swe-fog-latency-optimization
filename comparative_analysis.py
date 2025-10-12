"""
Comparative Analysis and Visualization
=====================================

This module provides comprehensive comparative analysis between fog architecture
and cloud-only architecture, including data analysis with Pandas and
visualization with Matplotlib.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from typing import Dict, List, Tuple, Any
import json
from datetime import datetime

# Import simulation modules
from fog_simulation import FogComputingSimulation, global_logger as fog_logger
from cloud_only_simulation import CloudOnlySimulation


class ComparativeAnalyzer:
    """
    Comprehensive comparative analysis between fog and cloud-only architectures.
    """
    
    def __init__(self):
        self.fog_data = None
        self.cloud_only_data = None
        self.fog_df = None
        self.cloud_only_df = None
        self.analysis_results = {}
    
    def run_comparative_simulation(self, simulation_time: float = 100.0, 
                                  num_fog_nodes: int = 3, num_iot_devices: int = 10):
        """
        Run both fog and cloud-only simulations for comparison.
        
        Args:
            simulation_time: Duration of both simulations
            num_fog_nodes: Number of fog nodes for fog simulation
            num_iot_devices: Number of IoT devices for both simulations
        """
        print("🚀 Running Comparative Analysis Simulations")
        print("=" * 60)
        
        # Run Fog Architecture Simulation
        print("\n🌫️  Running Fog Architecture Simulation...")
        fog_simulation = FogComputingSimulation(simulation_time=simulation_time)
        fog_simulation.setup_simulation(num_fog_nodes=num_fog_nodes, num_iot_devices=num_iot_devices)
        fog_simulation.run_simulation()
        fog_simulation.print_simulation_results()
        
        # Store fog data
        self.fog_data = fog_logger.export_data()
        
        # Run Cloud-Only Simulation
        print("\n☁️  Running Cloud-Only Architecture Simulation...")
        cloud_simulation = CloudOnlySimulation(simulation_time=simulation_time)
        cloud_simulation.setup_simulation(num_iot_devices=num_iot_devices)
        cloud_simulation.run_simulation()
        cloud_simulation.print_simulation_results()
        
        # Store cloud-only data
        self.cloud_only_data = cloud_simulation.performance_logger.export_data()
        
        print("\n✅ Both simulations completed successfully!")
        return fog_simulation, cloud_simulation
    
    def create_dataframes(self):
        """
        Convert simulation data to Pandas DataFrames for analysis.
        """
        print("\n📊 Creating DataFrames for Analysis...")
        
        # Create Fog Architecture DataFrame
        if self.fog_data and 'task_events' in self.fog_data:
            fog_events = self.fog_data['task_events']
            self.fog_df = pd.DataFrame(fog_events)
            
            # Calculate end-to-end latency for fog architecture
            self.fog_df = self._calculate_latency_metrics(self.fog_df, 'fog')
            print(f"   ✓ Fog Architecture DataFrame: {len(self.fog_df)} events")
        
        # Create Cloud-Only DataFrame
        if self.cloud_only_data and 'task_events' in self.cloud_only_data:
            cloud_events = self.cloud_only_data['task_events']
            self.cloud_only_df = pd.DataFrame(cloud_events)
            
            # Calculate end-to-end latency for cloud-only architecture
            self.cloud_only_df = self._calculate_latency_metrics(self.cloud_only_df, 'cloud_only')
            print(f"   ✓ Cloud-Only DataFrame: {len(self.cloud_only_df)} events")
        
        print("✅ DataFrames created successfully!")
    
    def _calculate_latency_metrics(self, df: pd.DataFrame, architecture: str) -> pd.DataFrame:
        """
        Calculate latency metrics for a given architecture.
        
        Args:
            df: DataFrame with task events
            architecture: Architecture type ('fog' or 'cloud_only')
            
        Returns:
            DataFrame with calculated latency metrics
        """
        # Group by task_id to calculate per-task metrics
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
    
    def calculate_performance_metrics(self):
        """
        Calculate comprehensive performance metrics for both architectures.
        """
        print("\n📈 Calculating Performance Metrics...")
        
        metrics = {}
        
        # Fog Architecture Metrics
        if self.fog_df is not None and not self.fog_df.empty:
            fog_metrics = {
                'average_latency': self.fog_df['end_to_end_latency'].mean(),
                'median_latency': self.fog_df['end_to_end_latency'].median(),
                'std_latency': self.fog_df['end_to_end_latency'].std(),
                'min_latency': self.fog_df['end_to_end_latency'].min(),
                'max_latency': self.fog_df['end_to_end_latency'].max(),
                'total_tasks': len(self.fog_df),
                'fog_processed': len(self.fog_df[self.fog_df['processing_location'].str.contains('FOG', na=False)]),
                'cloud_processed': len(self.fog_df[self.fog_df['processing_location'].str.contains('CLOUD', na=False)]),
                'offload_rate': len(self.fog_df[self.fog_df['decision_made'] == 'offload_to_cloud']) / len(self.fog_df) * 100 if len(self.fog_df) > 0 else 0
            }
            metrics['fog'] = fog_metrics
        
        # Cloud-Only Architecture Metrics
        if self.cloud_only_df is not None and not self.cloud_only_df.empty:
            cloud_metrics = {
                'average_latency': self.cloud_only_df['end_to_end_latency'].mean(),
                'median_latency': self.cloud_only_df['end_to_end_latency'].median(),
                'std_latency': self.cloud_only_df['end_to_end_latency'].std(),
                'min_latency': self.cloud_only_df['end_to_end_latency'].min(),
                'max_latency': self.cloud_only_df['end_to_end_latency'].max(),
                'total_tasks': len(self.cloud_only_df),
                'cloud_processed': len(self.cloud_only_df),
                'offload_rate': 100.0  # All tasks go to cloud
            }
            metrics['cloud_only'] = cloud_metrics
        
        self.analysis_results = metrics
        
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
    
    def create_visualizations(self, save_plots: bool = True):
        """
        Create comprehensive visualizations comparing both architectures.
        
        Args:
            save_plots: Whether to save plots to files
        """
        print("\n📊 Creating Comparative Visualizations...")
        
        # Set up the plotting style
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
        # Create figure with subplots
        fig = plt.figure(figsize=(20, 15))
        
        # 1. Bar Chart: Average End-to-End Latency Comparison
        ax1 = plt.subplot(2, 3, 1)
        self._create_latency_comparison_bar_chart(ax1)
        
        # 2. Scatter Plot: End-to-End Latency vs Task Complexity
        ax2 = plt.subplot(2, 3, 2)
        self._create_latency_complexity_scatter(ax2)
        
        # 3. Box Plot: Latency Distribution Comparison
        ax3 = plt.subplot(2, 3, 3)
        self._create_latency_distribution_boxplot(ax3)
        
        # 4. Processing Location Distribution
        ax4 = plt.subplot(2, 3, 4)
        self._create_processing_location_chart(ax4)
        
        # 5. Latency vs Time (if available)
        ax5 = plt.subplot(2, 3, 5)
        self._create_latency_timeline(ax5)
        
        # 6. Performance Metrics Summary
        ax6 = plt.subplot(2, 3, 6)
        self._create_metrics_summary_table(ax6)
        
        plt.tight_layout()
        
        if save_plots:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"comparative_analysis_{timestamp}.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"   ✓ Plots saved to: {filename}")
        
        plt.show()
        print("✅ Visualizations created successfully!")
    
    def _create_latency_comparison_bar_chart(self, ax):
        """Create bar chart comparing average latencies."""
        if self.analysis_results:
            architectures = []
            latencies = []
            
            if 'fog' in self.analysis_results:
                architectures.append('Fog Architecture')
                latencies.append(self.analysis_results['fog']['average_latency'])
            
            if 'cloud_only' in self.analysis_results:
                architectures.append('Cloud-Only')
                latencies.append(self.analysis_results['cloud_only']['average_latency'])
            
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
    
    def _create_latency_complexity_scatter(self, ax):
        """Create scatter plot of latency vs complexity."""
        if self.fog_df is not None and not self.fog_df.empty:
            # Plot fog data
            fog_data = self.fog_df[self.fog_df['architecture'] == 'fog']
            if not fog_data.empty:
                # Color by processing location
                fog_colors = ['#2E8B57' if 'FOG' in str(loc) else '#FF6347' for loc in fog_data['processing_location']]
                ax.scatter(fog_data['task_complexity'], fog_data['end_to_end_latency'], 
                          c=fog_colors, alpha=0.6, s=50, label='Fog Architecture', edgecolors='black', linewidth=0.5)
        
        if self.cloud_only_df is not None and not self.cloud_only_df.empty:
            # Plot cloud-only data
            ax.scatter(self.cloud_only_df['task_complexity'], self.cloud_only_df['end_to_end_latency'], 
                      c='#FF6347', alpha=0.6, s=50, label='Cloud-Only', marker='s', edgecolors='black', linewidth=0.5)
        
        ax.set_title('End-to-End Latency vs Task Complexity', fontsize=14, fontweight='bold')
        ax.set_xlabel('Task Complexity (MIPS)', fontsize=12)
        ax.set_ylabel('End-to-End Latency (seconds)', fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    def _create_latency_distribution_boxplot(self, ax):
        """Create box plot comparing latency distributions."""
        data_to_plot = []
        labels = []
        
        if self.fog_df is not None and not self.fog_df.empty:
            data_to_plot.append(self.fog_df['end_to_end_latency'].values)
            labels.append('Fog Architecture')
        
        if self.cloud_only_df is not None and not self.cloud_only_df.empty:
            data_to_plot.append(self.cloud_only_df['end_to_end_latency'].values)
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
    
    def _create_processing_location_chart(self, ax):
        """Create pie chart showing processing location distribution."""
        if self.fog_df is not None and not self.fog_df.empty:
            # Count processing locations
            location_counts = self.fog_df['processing_location'].value_counts()
            
            # Separate fog and cloud processing
            fog_count = sum(count for loc, count in location_counts.items() if 'FOG' in str(loc))
            cloud_count = sum(count for loc, count in location_counts.items() if 'CLOUD' in str(loc))
            
            sizes = [fog_count, cloud_count]
            labels = ['Fog Processing', 'Cloud Processing']
            colors = ['#2E8B57', '#FF6347']
            
            wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
            ax.set_title('Fog Architecture Processing Distribution', fontsize=14, fontweight='bold')
    
    def _create_latency_timeline(self, ax):
        """Create timeline showing latency over time."""
        if self.fog_df is not None and not self.fog_df.empty:
            # Sort by creation time
            timeline_data = self.fog_df.sort_values('creation_time')
            
            ax.plot(timeline_data['creation_time'], timeline_data['end_to_end_latency'], 
                   'o-', color='#2E8B57', alpha=0.7, markersize=4, label='Fog Architecture')
        
        if self.cloud_only_df is not None and not self.cloud_only_df.empty:
            timeline_data = self.cloud_only_df.sort_values('creation_time')
            
            ax.plot(timeline_data['creation_time'], timeline_data['end_to_end_latency'], 
                   's-', color='#FF6347', alpha=0.7, markersize=4, label='Cloud-Only')
        
        ax.set_title('Latency Timeline', fontsize=14, fontweight='bold')
        ax.set_xlabel('Simulation Time', fontsize=12)
        ax.set_ylabel('End-to-End Latency (seconds)', fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    def _create_metrics_summary_table(self, ax):
        """Create summary table of key metrics."""
        ax.axis('off')
        
        if self.analysis_results:
            # Create table data
            table_data = []
            
            if 'fog' in self.analysis_results:
                fog_metrics = self.analysis_results['fog']
                table_data.append(['Fog Architecture', f"{fog_metrics['average_latency']:.3f}s", 
                                 f"{fog_metrics['offload_rate']:.1f}%", f"{fog_metrics['total_tasks']}"])
            
            if 'cloud_only' in self.analysis_results:
                cloud_metrics = self.analysis_results['cloud_only']
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
    
    def export_analysis_results(self, filename: str = None):
        """
        Export analysis results to JSON file.
        
        Args:
            filename: Output filename (optional)
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"comparative_analysis_results_{timestamp}.json"
        
        export_data = {
            'analysis_timestamp': datetime.now().isoformat(),
            'analysis_results': self.analysis_results,
            'fog_dataframe_summary': self.fog_df.describe().to_dict() if self.fog_df is not None else None,
            'cloud_only_dataframe_summary': self.cloud_only_df.describe().to_dict() if self.cloud_only_df is not None else None
        }
        
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2, default=str)
        
        print(f"   ✓ Analysis results exported to: {filename}")
    
    def run_complete_analysis(self, simulation_time: float = 100.0, 
                             num_fog_nodes: int = 3, num_iot_devices: int = 10,
                             save_plots: bool = True):
        """
        Run complete comparative analysis including simulation, analysis, and visualization.
        
        Args:
            simulation_time: Duration of simulations
            num_fog_nodes: Number of fog nodes
            num_iot_devices: Number of IoT devices
            save_plots: Whether to save plots
        """
        print("🚀 Starting Complete Comparative Analysis")
        print("=" * 60)
        
        # Step 1: Run simulations
        self.run_comparative_simulation(simulation_time, num_fog_nodes, num_iot_devices)
        
        # Step 2: Create DataFrames
        self.create_dataframes()
        
        # Step 3: Calculate metrics
        self.calculate_performance_metrics()
        
        # Step 4: Create visualizations
        self.create_visualizations(save_plots)
        
        # Step 5: Export results
        self.export_analysis_results()
        
        print("\n🎉 Complete Comparative Analysis Finished!")
        print("✅ All analysis steps completed successfully!")


def main():
    """Main function to run comparative analysis."""
    analyzer = ComparativeAnalyzer()
    
    # Run complete analysis
    analyzer.run_complete_analysis(
        simulation_time=50.0,  # Shorter simulation for demo
        num_fog_nodes=3,
        num_iot_devices=8,
        save_plots=True
    )


if __name__ == "__main__":
    main()
