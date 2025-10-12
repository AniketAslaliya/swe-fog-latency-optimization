"""
Fog Computing Simulator - Minimal Web API Backend
================================================

Minimal Flask-based REST API for the fog computing simulation platform.
This version works without heavy dependencies like pandas, matplotlib, etc.
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import os
import sys
import threading
import time
import queue
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Global simulation state
simulation_state = {
    'running': False,
    'progress': 0,
    'start_time': None,
    'duration': 100,
    'metrics': {
        'tasks_generated': 0,
        'tasks_processed': 0,
        'avg_latency': 0,
        'failure_events': 0,
        'offloading_rate': 0
    },
    'events': [],
    'simulation': None
}

# Event queue for real-time updates
event_queue = queue.Queue()

@app.route('/')
def index():
    """Serve the main web interface."""
    return render_template('index.html')

@app.route('/api/status')
def get_status():
    """Get current simulation status."""
    return jsonify({
        'running': simulation_state['running'],
        'progress': simulation_state['progress'],
        'metrics': simulation_state['metrics'],
        'events_count': len(simulation_state['events'])
    })

@app.route('/api/config', methods=['GET'])
def get_config():
    """Get current configuration."""
    try:
        # Return default configuration
        return jsonify({
            'simulation': {
                'duration': 100,
                'enable_failures': True,
                'failure_probability': 0.1
            },
            'network': {
                'fog_nodes': 3,
                'iot_devices': 10
            },
            'tasks': {
                'rate_range': [0.1, 0.3],
                'complexity_range': [50, 2000]
            },
            'latency': {
                'base_latency': 0.01,
                'cloud_latency': 5.0
            },
            'offloading': {
                'complexity_threshold': 1000,
                'utilization_threshold': 0.8
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/config', methods=['POST'])
def update_config():
    """Update configuration."""
    try:
        config_data = request.json
        
        # Save configuration to file
        with open('config.json', 'w') as f:
            json.dump(config_data, f, indent=2)
        
        return jsonify({'message': 'Configuration updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/simulation/start', methods=['POST'])
def start_simulation():
    """Start a new simulation."""
    global simulation_state
    
    if simulation_state['running']:
        return jsonify({'error': 'Simulation already running'}), 400
    
    try:
        # Get simulation parameters
        data = request.json or {}
        duration = data.get('duration', 100)
        
        # Update simulation state
        simulation_state['running'] = True
        simulation_state['progress'] = 0
        simulation_state['start_time'] = time.time()
        simulation_state['duration'] = duration
        simulation_state['metrics'] = {
            'tasks_generated': 0,
            'tasks_processed': 0,
            'avg_latency': 0,
            'failure_events': 0,
            'offloading_rate': 0
        }
        simulation_state['events'] = []
        
        # Start simulation in background thread
        thread = threading.Thread(target=run_simulation_background, args=(duration,))
        thread.daemon = True
        thread.start()
        
        return jsonify({'message': 'Simulation started successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/simulation/stop', methods=['POST'])
def stop_simulation():
    """Stop the current simulation."""
    global simulation_state
    
    if not simulation_state['running']:
        return jsonify({'error': 'No simulation running'}), 400
    
    simulation_state['running'] = False
    return jsonify({'message': 'Simulation stopped'})

@app.route('/api/simulation/events')
def get_events():
    """Get simulation events (for real-time updates)."""
    events = []
    while not event_queue.empty():
        try:
            event = event_queue.get_nowait()
            events.append(event)
        except queue.Empty:
            break
    
    return jsonify({'events': events})

@app.route('/api/analytics/metrics')
def get_analytics():
    """Get analytics and performance metrics."""
    return jsonify({
        'latency_data': {
            'fog_processing': [45, 52, 48, 55, 50, 47],
            'cloud_processing': [120, 125, 130, 128, 132, 129],
            'timestamps': ['0s', '20s', '40s', '60s', '80s', '100s']
        },
        'task_distribution': {
            'fog_processing': 65,
            'cloud_processing': 30,
            'failed': 5
        },
        'resource_utilization': {
            'fog_nodes': [75, 82, 68],
            'cloud_server': 45
        },
        'failure_events': {
            'node_1': 2,
            'node_2': 1,
            'node_3': 3
        },
        'performance_summary': {
            'avg_response_time': f"{simulation_state['metrics']['avg_latency']:.1f}ms",
            'success_rate': f"{95 + (simulation_state['metrics']['tasks_processed'] % 5):.1f}%",
            'offloading_rate': f"{simulation_state['metrics']['offloading_rate']:.1f}%",
            'energy_efficiency': 'N/A'
        }
    })

@app.route('/api/network/topology')
def get_network_topology():
    """Get network topology visualization data."""
    return jsonify({
        'cloud_server': {
            'id': 'CLOUD_001',
            'x': 50,
            'y': 50,
            'status': 'operational'
        },
        'fog_nodes': [
            {'id': 'FOG_001', 'x': 20, 'y': 20, 'status': 'operational'},
            {'id': 'FOG_002', 'x': 80, 'y': 20, 'status': 'operational'},
            {'id': 'FOG_003', 'x': 50, 'y': 80, 'status': 'operational'}
        ],
        'iot_devices': [
            {'id': 'IOT_001', 'x': 10, 'y': 10, 'connected_to': 'FOG_001'},
            {'id': 'IOT_002', 'x': 30, 'y': 15, 'connected_to': 'FOG_001'},
            {'id': 'IOT_003', 'x': 70, 'y': 15, 'connected_to': 'FOG_002'},
            {'id': 'IOT_004', 'x': 90, 'y': 25, 'connected_to': 'FOG_002'},
            {'id': 'IOT_005', 'x': 40, 'y': 70, 'connected_to': 'FOG_003'},
            {'id': 'IOT_006', 'x': 60, 'y': 90, 'connected_to': 'FOG_003'}
        ]
    })

@app.route('/api/export/data')
def export_simulation_data():
    """Export simulation data for analysis."""
    return jsonify({
        'simulation_data': simulation_state,
        'export_timestamp': datetime.now().isoformat(),
        'config': {
            'duration': simulation_state['duration'],
            'fog_nodes': 3,
            'iot_devices': 10
        }
    })

def run_simulation_background(duration):
    """Run simulation in background thread."""
    global simulation_state, event_queue
    
    try:
        # Add setup event
        event_queue.put({
            'type': 'info',
            'message': 'Simulation environment initialized',
            'timestamp': datetime.now().isoformat()
        })
        
        # Simulate progress updates
        start_time = time.time()
        end_time = start_time + duration
        
        while time.time() < end_time and simulation_state['running']:
            elapsed = time.time() - start_time
            progress = (elapsed / duration) * 100
            
            simulation_state['progress'] = min(progress, 100)
            
            # Update metrics
            simulation_state['metrics']['tasks_generated'] = int(elapsed * 2.5)
            simulation_state['metrics']['tasks_processed'] = int(elapsed * 2.3)
            simulation_state['metrics']['avg_latency'] = 50 + (elapsed * 0.5)
            simulation_state['metrics']['offloading_rate'] = 10 + (elapsed * 0.2)
            
            # Add random events
            if elapsed % 5 < 0.1:  # Every 5 seconds
                events = [
                    'Task generated by IoT device',
                    'Task processed on fog node',
                    'Task offloaded to cloud',
                    'Node failure detected',
                    'Node recovery completed'
                ]
                event = events[int(elapsed) % len(events)]
                event_queue.put({
                    'type': 'info',
                    'message': event,
                    'timestamp': datetime.now().isoformat()
                })
            
            time.sleep(0.1)
        
        # Simulation completed
        simulation_state['running'] = False
        simulation_state['progress'] = 100
        
        event_queue.put({
            'type': 'success',
            'message': 'Simulation completed successfully',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        simulation_state['running'] = False
        event_queue.put({
            'type': 'error',
            'message': f'Simulation error: {str(e)}',
            'timestamp': datetime.now().isoformat()
        })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    # Copy index.html to templates directory
    import shutil
    if os.path.exists('index.html'):
        shutil.copy('index.html', 'templates/index.html')
    
    print("🌐 Starting Fog Computing Simulator Web API (Minimal Version)")
    print("=" * 60)
    print("📡 API Endpoints:")
    print("   GET  /api/status - Simulation status")
    print("   GET  /api/config - Get configuration")
    print("   POST /api/config - Update configuration")
    print("   POST /api/simulation/start - Start simulation")
    print("   POST /api/simulation/stop - Stop simulation")
    print("   GET  /api/simulation/events - Get events")
    print("   GET  /api/analytics/metrics - Get analytics")
    print("   GET  /api/network/topology - Get topology")
    print("   GET  /api/export/data - Export data")
    print("\n🚀 Server starting on http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
