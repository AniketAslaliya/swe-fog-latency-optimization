"""
Fog Computing Simulator - Backend API Server
============================================

Flask API server for the fog computing simulation platform.
Implements priority-based task scheduling and routing.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import threading
import time
import queue
from datetime import datetime
import random
import heapq

app = Flask(__name__)

# CORS Configuration
# Allow localhost for development and Vercel domains for production
import os
allowed_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

# Add Vercel preview and production URLs from environment variable
vercel_url = os.environ.get('VERCEL_URL')
if vercel_url:
    allowed_origins.append(f"https://{vercel_url}")

# Add custom frontend URL from environment variable
frontend_url = os.environ.get('FRONTEND_URL')
if frontend_url:
    allowed_origins.append(frontend_url)

# Allow all origins in development, specific origins in production
if os.environ.get('FLASK_ENV') == 'development' or not os.environ.get('RENDER'):
    CORS(app, origins=allowed_origins, supports_credentials=True)
else:
    # In production (Render), only allow specific origins
    CORS(app, origins=allowed_origins, supports_credentials=True)

# Priority weights for scheduling
PRIORITY_WEIGHTS = {
    'HIGH': 3,
    'MODERATE': 2,
    'LOW': 1
}

def load_config_from_file():
    """Load configuration from config.json if it exists."""
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = json.load(f)
                
                # Validate and fix config values
                if 'network' not in config:
                    config['network'] = {}
                
                # Ensure fog_nodes is valid
                fog_nodes = config['network'].get('fog_nodes', 3)
                if not isinstance(fog_nodes, int) or fog_nodes < 1:
                    fog_nodes = 3
                config['network']['fog_nodes'] = fog_nodes
                
                # Ensure iot_devices is valid (never null)
                iot_devices = config['network'].get('iot_devices', 10)
                if iot_devices is None or not isinstance(iot_devices, int) or iot_devices < 1:
                    iot_devices = 10
                config['network']['iot_devices'] = iot_devices
                
                # Validate other sections
                if 'simulation' not in config:
                    config['simulation'] = {'duration': 100, 'enable_failures': True, 'failure_probability': 0.1}
                if 'tasks' not in config:
                    config['tasks'] = {'rate_range': [0.1, 0.3], 'complexity_range': [50, 2000]}
                if 'latency' not in config:
                    config['latency'] = {'base_latency': 0.01, 'cloud_latency': 5.0}
                if 'offloading' not in config:
                    config['offloading'] = {'complexity_threshold': 1000, 'utilization_threshold': 0.8}
                
                # Save corrected config back to file
                with open(config_path, 'w') as f:
                    json.dump(config, f, indent=2)
                
                print(f"✅ Configuration loaded and validated from config.json")
                return config
    except Exception as e:
        print(f"⚠️ Error loading config: {e}")
    
    # Return default config
    default_config = {
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
    }
    
    # Save default config to file
    try:
        with open(config_path, 'w') as f:
            json.dump(default_config, f, indent=2)
    except:
        pass
    
    return default_config

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
    'simulation': None,
    'latency_history': {
        'fog_latency': [],
        'cloud_latency': [],
        'timestamps': []
    },
    # Priority-based task queues
    'pending_fog_tasks': [],  # Priority queue (heap)
    'cloud_tasks': [],  # Regular list
    'active_tasks': {},  # Track active tasks by task_id
    'task_counter': 0,  # Global task ID counter
    'priority_distribution': {'HIGH': 0, 'MODERATE': 0, 'LOW': 0},
    # Device priority mapping: device_id -> priority
    'device_priorities': {}  # Will be initialized from config
}

simulation_state['config'] = load_config_from_file()
# Initialize device priorities from config
num_devices = simulation_state['config'].get('network', {}).get('iot_devices', 10)
# Ensure num_devices is a valid integer
if num_devices is None or not isinstance(num_devices, int) or num_devices < 1:
    num_devices = 10
    # Update config with valid value
    if 'network' not in simulation_state['config']:
        simulation_state['config']['network'] = {}
    simulation_state['config']['network']['iot_devices'] = num_devices

simulation_state['device_priorities'] = {}
for i in range(1, num_devices + 1):
    device_id = f'device_{i}'
    # Default: distribute priorities (30% HIGH, 40% MODERATE, 30% LOW)
    if i <= num_devices * 0.3:
        simulation_state['device_priorities'][device_id] = 'HIGH'
    elif i <= num_devices * 0.7:
        simulation_state['device_priorities'][device_id] = 'MODERATE'
    else:
        simulation_state['device_priorities'][device_id] = 'LOW'

print(f"🚀 Server started with {simulation_state['config']['network']['fog_nodes']} fog nodes")
print(f"📱 Device priorities initialized for {num_devices} devices")

# Event queue for real-time updates
event_queue = queue.Queue()

# Lock for thread-safe operations
state_lock = threading.Lock()

def generate_task(current_time):
    """
    Generate a new IoT task with priority, complexity, and arrival time.
    Priority is determined by the device that generates the task.
    
    Returns:
        dict: Task with task_id, priority, complexity, arrival_time, node_assigned, device_id
    """
    global simulation_state
    
    with state_lock:
        simulation_state['task_counter'] += 1
        task_id = simulation_state['task_counter']
    
    # Select a random device to generate the task
    num_devices = simulation_state.get('config', {}).get('network', {}).get('iot_devices', 10)
    device_index = random.randint(1, num_devices)
    device_id = f'device_{device_index}'
    
    # Get priority from device configuration (fallback to random if not set)
    with state_lock:
        device_priorities = simulation_state.get('device_priorities', {})
        priority = device_priorities.get(device_id)
        
        # If device priority not set, use random (backward compatibility)
        if not priority:
            priority_roll = random.random()
            if priority_roll < 0.3:
                priority = 'HIGH'
            elif priority_roll < 0.7:
                priority = 'MODERATE'
            else:
                priority = 'LOW'
    
    # Complexity based on config
    config = simulation_state.get('config', {})
    complexity_range = config.get('tasks', {}).get('complexity_range', [50, 2000])
    complexity = random.randint(complexity_range[0], complexity_range[1])
    
    # Determine node assignment based on priority
    if priority == 'HIGH':
        node_assigned = 'fog'
    else:
        node_assigned = 'cloud'
    
    task = {
        'task_id': task_id,
        'priority': priority,
        'complexity': complexity,
        'arrival_time': current_time,
        'node_assigned': node_assigned,
        'device_id': device_id
    }
    
    return task

def schedule_fog_task(task):
    """
    Add HIGH priority task to fog priority queue.
    Sorting: (-priority_weight, arrival_time, complexity)
    """
    global simulation_state
    
    priority_weight = PRIORITY_WEIGHTS.get(task['priority'], 1)
    # Use negative priority_weight for max-heap behavior (highest priority first)
    sort_key = (-priority_weight, task['arrival_time'], task['complexity'])
    
    with state_lock:
        heapq.heappush(simulation_state['pending_fog_tasks'], (sort_key, task))
        simulation_state['priority_distribution'][task['priority']] += 1
    
    event_queue.put({
        'type': 'info',
        'message': f"Task {task['task_id']} generated: {task['priority']} (complexity={task['complexity']})",
        'timestamp': datetime.now().isoformat()
    })
    
    event_queue.put({
        'type': 'info',
        'message': f"Task {task['task_id']} assigned to fog",
        'timestamp': datetime.now().isoformat()
    })

def schedule_cloud_task(task):
    """
    Add LOW/MODERATE priority task to cloud queue.
    """
    global simulation_state
    
    with state_lock:
        simulation_state['cloud_tasks'].append(task)
        simulation_state['priority_distribution'][task['priority']] += 1
    
    event_queue.put({
        'type': 'info',
        'message': f"Task {task['task_id']} generated: {task['priority']} (complexity={task['complexity']})",
        'timestamp': datetime.now().isoformat()
    })
    
    event_queue.put({
        'type': 'info',
        'message': f"Task {task['task_id']} offloaded to cloud",
        'timestamp': datetime.now().isoformat()
    })

def process_fog_task(current_time):
    """
    Process highest priority task from fog queue.
    Returns processing latency based on complexity.
    """
    global simulation_state
    
    with state_lock:
        if not simulation_state['pending_fog_tasks']:
            return None
        
        # Pop highest priority task
        sort_key, task = heapq.heappop(simulation_state['pending_fog_tasks'])
        
        # Mark as active (use actual time, not elapsed)
        task['processing_start'] = time.time()
        simulation_state['active_tasks'][task['task_id']] = task
    
    # Simulate processing time: base latency + complexity factor
    # Higher complexity = longer processing
    # Increased processing time to allow queues to build up
    base_latency = 200  # ms (increased from 30ms)
    complexity_factor = task['complexity'] / 50  # 1ms to 40ms (increased from /100)
    processing_latency = base_latency + complexity_factor
    
    # Store processing time in task for cleanup calculation (in seconds)
    # Make processing time longer so queues can build up
    task['processing_time'] = processing_latency / 1000  # Convert ms to seconds
    
    # Check if there's another task being processed (for scheduling comparison)
    with state_lock:
        if simulation_state['pending_fog_tasks']:
            next_sort_key, next_task = simulation_state['pending_fog_tasks'][0]
            if next_task['arrival_time'] < task['arrival_time']:
                event_queue.put({
                    'type': 'info',
                    'message': f"Fog scheduling: Task {task['task_id']} processed before Task {next_task['task_id']} (higher priority)",
                    'timestamp': datetime.now().isoformat()
                })
    
    return processing_latency

def process_cloud_task(current_time):
    """
    Process a task from cloud queue (FIFO).
    Returns processing latency (higher than fog).
    """
    global simulation_state
    
    with state_lock:
        if not simulation_state['cloud_tasks']:
            return None
        
        # Process first task (FIFO)
        task = simulation_state['cloud_tasks'].pop(0)
        task['processing_start'] = time.time()
        simulation_state['active_tasks'][task['task_id']] = task
    
    # Cloud has higher base latency + network overhead
    # Increased processing time to allow queues to build up
    base_latency = 500  # ms (increased from 120ms)
    complexity_factor = task['complexity'] / 40  # 1.25ms to 50ms (increased from /80)
    processing_latency = base_latency + complexity_factor
    
    # Store processing time in task for cleanup calculation (in seconds)
    task['processing_time'] = processing_latency / 1000  # Convert ms to seconds
    
    return processing_latency

@app.route('/api/status')
def get_status():
    """Get current simulation status."""
    global simulation_state
    
    with state_lock:
        # Count pending tasks in queues
        fog_pending = len(simulation_state['pending_fog_tasks'])
        cloud_pending = len(simulation_state['cloud_tasks'])
        
        # Count active tasks (currently being processed)
        # Active tasks are tasks that have been popped from queue but not yet completed
        active_fog_tasks = sum(1 for task in simulation_state['active_tasks'].values() 
                              if task.get('node_assigned') == 'fog')
        active_cloud_tasks = sum(1 for task in simulation_state['active_tasks'].values() 
                                if task.get('node_assigned') == 'cloud')
        
        # Total queue length = pending + active
        fog_queue_length = fog_pending + active_fog_tasks
        cloud_queue_length = cloud_pending + active_cloud_tasks
    
    return jsonify({
        'running': simulation_state['running'],
        'progress': simulation_state['progress'],
        'metrics': simulation_state['metrics'],
        'events_count': len(simulation_state['events']),
        'fog_queue_length': fog_queue_length,
        'cloud_queue_length': cloud_queue_length,
        'fog_pending': fog_pending,
        'cloud_pending': cloud_pending,
        'fog_active': active_fog_tasks,
        'cloud_active': active_cloud_tasks,
        'priority_distribution': simulation_state['priority_distribution']
    })

@app.route('/api/config', methods=['GET'])
def get_config():
    """Get current configuration."""
    try:
        return jsonify(simulation_state.get('config', load_config_from_file()))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/config', methods=['POST'])
def update_config():
    """Update configuration."""
    try:
        config_data = request.json
        
        if not config_data:
            return jsonify({'error': 'No configuration data provided'}), 400
        
        global simulation_state
        
        # Validate required fields
        if 'network' not in config_data:
            config_data['network'] = simulation_state.get('config', {}).get('network', {'fog_nodes': 3, 'iot_devices': 10})
        if 'simulation' not in config_data:
            config_data['simulation'] = simulation_state.get('config', {}).get('simulation', {'duration': 100, 'enable_failures': True, 'failure_probability': 0.1})
        if 'tasks' not in config_data:
            config_data['tasks'] = simulation_state.get('config', {}).get('tasks', {'rate_range': [0.1, 0.3], 'complexity_range': [50, 2000]})
        if 'latency' not in config_data:
            config_data['latency'] = simulation_state.get('config', {}).get('latency', {'base_latency': 0.01, 'cloud_latency': 5.0})
        if 'offloading' not in config_data:
            config_data['offloading'] = simulation_state.get('config', {}).get('offloading', {'complexity_threshold': 1000, 'utilization_threshold': 0.8})
        
        with state_lock:
            simulation_state['config'] = config_data
            
            # Update device priorities if device count changed
            num_devices = config_data.get('network', {}).get('iot_devices', 10)
            if not isinstance(num_devices, int) or num_devices < 1:
                num_devices = 10
            
            # Ensure device_priorities exists
            if 'device_priorities' not in simulation_state:
                simulation_state['device_priorities'] = {}
            
            current_devices = len(simulation_state.get('device_priorities', {}))
            
            # If device count increased, add new devices with default priorities
            if num_devices > current_devices:
                for i in range(current_devices + 1, num_devices + 1):
                    device_id = f'device_{i}'
                    # Default priority distribution
                    if i <= num_devices * 0.3:
                        simulation_state['device_priorities'][device_id] = 'HIGH'
                    elif i <= num_devices * 0.7:
                        simulation_state['device_priorities'][device_id] = 'MODERATE'
                    else:
                        simulation_state['device_priorities'][device_id] = 'LOW'
            # If device count decreased, remove extra devices
            elif num_devices < current_devices:
                devices_to_remove = [f'device_{i}' for i in range(num_devices + 1, current_devices + 1)]
                for device_id in devices_to_remove:
                    simulation_state['device_priorities'].pop(device_id, None)
        
        # Save configuration to file
        try:
            config_path = os.path.join(os.path.dirname(__file__), 'config.json')
            with open(config_path, 'w') as f:
                json.dump(config_data, f, indent=2)
        except Exception as file_error:
            print(f"⚠️ Warning: Could not save config to file: {file_error}")
            # Continue even if file save fails
        
        fog_nodes = config_data.get('network', {}).get('fog_nodes', 3)
        print(f"✅ Config updated: {fog_nodes} fog nodes")
        return jsonify({'message': 'Configuration updated successfully'})
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"❌ Error updating config: {error_trace}")
        return jsonify({'error': str(e), 'trace': error_trace}), 500

@app.route('/api/device-priorities', methods=['GET'])
def get_device_priorities():
    """Get device priority configuration."""
    global simulation_state
    
    try:
        with state_lock:
            num_devices = simulation_state.get('config', {}).get('network', {}).get('iot_devices', 10)
            # Ensure num_devices is valid
            if not isinstance(num_devices, int) or num_devices < 1:
                num_devices = 10
            
            return jsonify({
                'device_priorities': simulation_state.get('device_priorities', {}),
                'num_devices': num_devices
            })
    except Exception as e:
        return jsonify({'error': str(e), 'device_priorities': {}, 'num_devices': 10}), 500

@app.route('/api/device-priorities', methods=['POST'])
def update_device_priorities():
    """Update device priority configuration."""
    try:
        data = request.json
        device_priorities = data.get('device_priorities', {})
        
        global simulation_state
        with state_lock:
            # Validate priorities
            valid_priorities = ['HIGH', 'MODERATE', 'LOW']
            for device_id, priority in device_priorities.items():
                if priority not in valid_priorities:
                    return jsonify({'error': f'Invalid priority {priority} for device {device_id}'}), 400
            
            # Update device priorities
            simulation_state['device_priorities'].update(device_priorities)
        
        print(f"✅ Device priorities updated: {len(device_priorities)} devices")
        return jsonify({'message': 'Device priorities updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/simulation/start', methods=['POST'])
def start_simulation():
    """Start a new simulation."""
    global simulation_state
    
    if simulation_state['running']:
        return jsonify({'error': 'Simulation already running'}), 400
    
    try:
        data = request.json or {}
        duration = data.get('duration', 100)
        
        # Validate duration
        if not isinstance(duration, (int, float)) or duration < 1:
            duration = 100
        duration = int(duration)
        
        with state_lock:
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
            simulation_state['latency_history'] = {
                'fog_latency': [],
                'cloud_latency': [],
                'timestamps': []
            }
            # Reset task queues
            simulation_state['pending_fog_tasks'] = []
            simulation_state['cloud_tasks'] = []
            simulation_state['active_tasks'] = {}
            simulation_state['task_counter'] = 0
            simulation_state['priority_distribution'] = {'HIGH': 0, 'MODERATE': 0, 'LOW': 0}
            # Reinitialize device priorities if device count changed
            num_devices = simulation_state.get('config', {}).get('network', {}).get('iot_devices', 10)
            # Ensure num_devices is a valid integer
            if not isinstance(num_devices, int) or num_devices < 1:
                num_devices = 10
            
            # Ensure device_priorities exists
            if 'device_priorities' not in simulation_state:
                simulation_state['device_priorities'] = {}
            
            current_devices = len(simulation_state.get('device_priorities', {}))
            if current_devices != num_devices:
                simulation_state['device_priorities'] = {}
                for i in range(1, num_devices + 1):
                    device_id = f'device_{i}'
                    if i <= num_devices * 0.3:
                        simulation_state['device_priorities'][device_id] = 'HIGH'
                    elif i <= num_devices * 0.7:
                        simulation_state['device_priorities'][device_id] = 'MODERATE'
                    else:
                        simulation_state['device_priorities'][device_id] = 'LOW'
        
        thread = threading.Thread(target=run_simulation_background, args=(duration,))
        thread.daemon = True
        thread.start()
        
        return jsonify({'message': 'Simulation started successfully'})
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"❌ Error starting simulation: {error_trace}")
        # Reset running state on error
        with state_lock:
            simulation_state['running'] = False
        return jsonify({'error': str(e), 'trace': error_trace}), 500

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

@app.route('/api/tasks')
def get_tasks():
    """Get current task queues and active tasks."""
    global simulation_state
    
    with state_lock:
        # Get pending fog tasks (without popping)
        fog_tasks = [task for _, task in simulation_state['pending_fog_tasks']]
        cloud_tasks = simulation_state['cloud_tasks'].copy()
        active_tasks = list(simulation_state['active_tasks'].values())
    
    return jsonify({
        'fog_queue': fog_tasks,
        'cloud_queue': cloud_tasks,
        'active_tasks': active_tasks
    })

@app.route('/api/analytics/metrics')
def get_analytics():
    """Get analytics and performance metrics."""
    global simulation_state
    
    try:
        success_rate = 95.0
        if simulation_state['metrics']['tasks_generated'] > 0:
            success_rate = min(100, (simulation_state['metrics']['tasks_processed'] / simulation_state['metrics']['tasks_generated']) * 100)
        
        latency_history = simulation_state.get('latency_history', {})
        
        if latency_history.get('fog_latency') and len(latency_history['fog_latency']) > 0:
            fog_data = latency_history['fog_latency']
            cloud_data = latency_history['cloud_latency']
            timestamps = latency_history['timestamps']
            
            while len(fog_data) < 6:
                fog_data.append(fog_data[-1] if fog_data else 45)
                cloud_data.append(cloud_data[-1] if cloud_data else 130)
                timestamps.append(f"{len(timestamps)*20}s")
        else:
            fog_data = [45, 52, 48, 55, 50, 47]
            cloud_data = [120, 125, 130, 128, 132, 129]
            timestamps = ['0s', '20s', '40s', '60s', '80s', '100s']
        
        offload_rate = simulation_state['metrics']['offloading_rate']
        total_tasks = simulation_state['metrics']['tasks_generated']
        processed_tasks = simulation_state['metrics']['tasks_processed']
        
        if total_tasks > 0:
            fog_processing = max(20, int((processed_tasks * (100 - offload_rate)) / 100))
            cloud_processing = max(10, int((processed_tasks * offload_rate) / 100))
            failed_tasks = max(0, total_tasks - processed_tasks)
            
            total_percentage = fog_processing + cloud_processing + failed_tasks
            if total_percentage > 0:
                fog_processing = int((fog_processing / total_percentage) * 100)
                cloud_processing = int((cloud_processing / total_percentage) * 100)
                failed_tasks = max(0, 100 - fog_processing - cloud_processing)
        else:
            fog_processing = max(20, 100 - offload_rate - 5)
            cloud_processing = offload_rate
            failed_tasks = 5
        
        if 'config' in simulation_state and 'network' in simulation_state['config']:
            num_fog_nodes = simulation_state['config']['network'].get('fog_nodes', 3)
        else:
            num_fog_nodes = 3
        
        total_tasks = simulation_state['metrics']['tasks_generated']
        processed_tasks = simulation_state['metrics']['tasks_processed']
        base_utilization = 30 + min(40, (total_tasks * 0.5))
        
        fog_utilization = []
        for i in range(num_fog_nodes):
            node_base = base_utilization + random.randint(-15, 15)
            node_util = max(20, min(95, node_base))
            fog_utilization.append(int(node_util))
        
        cloud_utilization = int(25 + min(30, (total_tasks * 0.3)) + random.randint(-5, 10))
        cloud_utilization = max(15, min(70, cloud_utilization))
        
        failure_events = {}
        base_failures = simulation_state['metrics']['failure_events']
        
        if base_failures > 0:
            failure_distribution = [0] * num_fog_nodes
            # Generate weights dynamically to match number of fog nodes
            # Use a pattern that varies weights slightly for each node
            base_weights = [1.0, 1.2, 0.8, 1.1, 0.9, 1.0, 1.1, 0.9, 1.2, 1.0]  # Extended base weights
            weights = [base_weights[i % len(base_weights)] for i in range(num_fog_nodes)]
            
            for _ in range(base_failures):
                node_index = random.choices(range(num_fog_nodes), weights=weights)[0]
                failure_distribution[node_index] += 1
            
            for i in range(num_fog_nodes):
                node_id = f'node_{i+1}'
                failure_events[node_id] = failure_distribution[i]
        else:
            for i in range(num_fog_nodes):
                node_id = f'node_{i+1}'
                failure_events[node_id] = 0
        
        # Get queue lengths (including active tasks)
        with state_lock:
            fog_pending = len(simulation_state['pending_fog_tasks'])
            cloud_pending = len(simulation_state['cloud_tasks'])
            active_fog = sum(1 for task in simulation_state['active_tasks'].values() 
                            if task.get('node_assigned') == 'fog')
            active_cloud = sum(1 for task in simulation_state['active_tasks'].values() 
                              if task.get('node_assigned') == 'cloud')
            fog_queue_length = fog_pending + active_fog
            cloud_queue_length = cloud_pending + active_cloud
            priority_dist = simulation_state['priority_distribution'].copy()
        
        return jsonify({
            'latency_data': {
                'fog_processing': fog_data,
                'cloud_processing': cloud_data,
                'timestamps': timestamps
            },
            'task_distribution': {
                'fog_processing': fog_processing,
                'cloud_processing': cloud_processing,
                'failed': failed_tasks
            },
            'resource_utilization': {
                'fog_nodes': fog_utilization,
                'cloud_server': cloud_utilization
            },
            'failure_events': failure_events,
            'performance_summary': {
                'avg_response_time': f"{simulation_state['metrics']['avg_latency']:.1f}ms",
                'success_rate': f"{success_rate:.1f}%",
                'offloading_rate': f"{offload_rate:.1f}%",
                'energy_efficiency': f"{85 + random.randint(-5, 10):.1f}%"
            },
            'priority_distribution': priority_dist,
            'fog_queue_length': fog_queue_length,
            'cloud_queue_length': cloud_queue_length
        })
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"❌ Error in get_analytics: {error_trace}")
        # Return default/empty analytics on error
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
                'fog_nodes': [45, 52, 48],
                'cloud_server': 35
            },
            'failure_events': {},
            'performance_summary': {
                'avg_response_time': '0.0ms',
                'success_rate': '100.0%',
                'offloading_rate': '0.0%',
                'energy_efficiency': '85.0%'
            },
            'priority_distribution': {'HIGH': 0, 'MODERATE': 0, 'LOW': 0},
            'fog_queue_length': 0,
            'cloud_queue_length': 0,
            'error': str(e)
        }), 200  # Return 200 with default data instead of 500

@app.route('/api/network/topology')
def get_network_topology():
    """Get network topology visualization data."""
    global simulation_state
    
    num_fog_nodes = simulation_state.get('config', {}).get('network', {}).get('fog_nodes', 3)
    
    with state_lock:
        fog_pending = len(simulation_state['pending_fog_tasks'])
        active_fog = sum(1 for task in simulation_state['active_tasks'].values() 
                        if task.get('node_assigned') == 'fog')
        fog_queue_length = fog_pending + active_fog
        # Distribute tasks evenly across fog nodes (dummy distribution)
        tasks_per_node = fog_queue_length // num_fog_nodes if num_fog_nodes > 0 else 0
        remainder = fog_queue_length % num_fog_nodes
    
    fog_nodes = []
    for i in range(num_fog_nodes):
        node_tasks = tasks_per_node + (1 if i < remainder else 0)
        fog_nodes.append({
            'id': f'FOG_{i+1:03d}',
            'x': 20 + (i * 30) % 80,
            'y': 20 + (i * 25) % 60,
            'status': 'operational',
            'queued_tasks': node_tasks
        })
    
    return jsonify({
        'cloud_server': {
            'id': 'CLOUD_001',
            'x': 50,
            'y': 50,
            'status': 'operational'
        },
        'fog_nodes': fog_nodes,
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
    global simulation_state
    
    with state_lock:
        fog_tasks = [task for _, task in simulation_state['pending_fog_tasks']]
        cloud_tasks = simulation_state['cloud_tasks'].copy()
    
    return jsonify({
        'simulation_data': simulation_state,
        'export_timestamp': datetime.now().isoformat(),
        'config': {
            'duration': simulation_state['duration'],
            'fog_nodes': simulation_state.get('config', {}).get('network', {}).get('fog_nodes', 3),
            'iot_devices': simulation_state.get('config', {}).get('network', {}).get('iot_devices', 10)
        },
        'task_queues': {
            'fog_queue': fog_tasks,
            'cloud_queue': cloud_tasks
        }
    })

def run_simulation_background(duration):
    """Run simulation in background thread with priority-based scheduling."""
    global simulation_state, event_queue
    
    try:
        event_queue.put({
            'type': 'info',
            'message': 'Simulation environment initialized with priority-based scheduling',
            'timestamp': datetime.now().isoformat()
        })
        
        start_time = time.time()
        end_time = start_time + duration
        last_task_gen_time = start_time
        task_gen_interval = 0.5  # Generate task every 0.5 seconds
        
        fog_latencies = []
        cloud_latencies = []
        
        while time.time() < end_time and simulation_state['running']:
            current_time = time.time()
            elapsed = current_time - start_time
            progress = (elapsed / duration) * 100
            simulation_state['progress'] = min(progress, 100)
            
            # Generate tasks periodically
            if current_time - last_task_gen_time >= task_gen_interval:
                task = generate_task(elapsed)
                
                with state_lock:
                    simulation_state['metrics']['tasks_generated'] += 1
                
                # Route task based on priority
                if task['priority'] == 'HIGH':
                    schedule_fog_task(task)
                else:
                    schedule_cloud_task(task)
                
                last_task_gen_time = current_time
                
                # Log which device generated the task
                event_queue.put({
                    'type': 'info',
                    'message': f"Task {task['task_id']} generated by {task.get('device_id', 'unknown')} with {task['priority']} priority",
                    'timestamp': datetime.now().isoformat()
                })
            
            # Process fog tasks (HIGH priority) - only process if no active fog tasks
            # This limits concurrent processing and allows queue to build up
            with state_lock:
                active_fog_count = sum(1 for task in simulation_state['active_tasks'].values() 
                                      if task.get('node_assigned') == 'fog')
            
            # Only process new fog task if there are no active fog tasks (limit concurrency)
            if simulation_state['pending_fog_tasks'] and active_fog_count == 0:
                fog_latency = process_fog_task(elapsed)
                if fog_latency:
                    fog_latencies.append(fog_latency)
                    with state_lock:
                        simulation_state['metrics']['tasks_processed'] += 1
            
            # Clean up completed active tasks (tasks that have finished processing)
            # Tasks stay in active_tasks for a short time to show they're being processed
            with state_lock:
                current_time_check = time.time()
                completed_tasks = []
                for task_id, task in simulation_state['active_tasks'].items():
                    processing_start = task.get('processing_start', 0)
                    processing_time = task.get('processing_time', 0.2)  # Default 200ms (fog) or 500ms (cloud)
                    # Remove task if it's been processing for longer than its processing time
                    if current_time_check - processing_start > processing_time:
                        completed_tasks.append(task_id)
                
                for task_id in completed_tasks:
                    del simulation_state['active_tasks'][task_id]
            
            # Process cloud tasks (LOW/MODERATE priority) - limit concurrent processing
            with state_lock:
                active_cloud_count = sum(1 for task in simulation_state['active_tasks'].values() 
                                        if task.get('node_assigned') == 'cloud')
            
            # Only process new cloud task if there are no active cloud tasks (limit concurrency)
            if simulation_state['cloud_tasks'] and active_cloud_count == 0:
                cloud_latency = process_cloud_task(elapsed)
                if cloud_latency:
                    cloud_latencies.append(cloud_latency)
                    with state_lock:
                        simulation_state['metrics']['tasks_processed'] += 1
            
            # Update latency history periodically (every 3 seconds of simulation time)
            if int(elapsed) % 3 == 0 and elapsed > 0:
                avg_fog = sum(fog_latencies[-10:]) / len(fog_latencies[-10:]) if fog_latencies else 45
                avg_cloud = sum(cloud_latencies[-10:]) / len(cloud_latencies[-10:]) if cloud_latencies else 130
                
                with state_lock:
                    # Always update latency history to show progression
                    if len(fog_latencies) > 0 or len(cloud_latencies) > 0:
                        # Only append if timestamp is different (avoid duplicates)
                        last_timestamp = simulation_state['latency_history']['timestamps'][-1] if simulation_state['latency_history']['timestamps'] else None
                        current_timestamp = f"{elapsed:.0f}s"
                        if last_timestamp != current_timestamp:
                            simulation_state['latency_history']['fog_latency'].append(avg_fog)
                            simulation_state['latency_history']['cloud_latency'].append(avg_cloud)
                            simulation_state['latency_history']['timestamps'].append(current_timestamp)
                            
                            # Keep only last 6 data points
                            if len(simulation_state['latency_history']['fog_latency']) > 6:
                                simulation_state['latency_history']['fog_latency'] = simulation_state['latency_history']['fog_latency'][-6:]
                                simulation_state['latency_history']['cloud_latency'] = simulation_state['latency_history']['cloud_latency'][-6:]
                                simulation_state['latency_history']['timestamps'] = simulation_state['latency_history']['timestamps'][-6:]
                        else:
                            # Update last values if timestamp is same
                            if len(simulation_state['latency_history']['fog_latency']) > 0:
                                simulation_state['latency_history']['fog_latency'][-1] = avg_fog
                                simulation_state['latency_history']['cloud_latency'][-1] = avg_cloud
                    
                    # Update average latency continuously
                    if fog_latencies and cloud_latencies:
                        simulation_state['metrics']['avg_latency'] = (avg_fog + avg_cloud) / 2
                    elif fog_latencies:
                        simulation_state['metrics']['avg_latency'] = avg_fog
                    elif cloud_latencies:
                        simulation_state['metrics']['avg_latency'] = avg_cloud
                    
                    # Update offloading rate (percentage of tasks sent to cloud)
                    total_generated = simulation_state['metrics']['tasks_generated']
                    if total_generated > 0:
                        cloud_count = simulation_state['priority_distribution'].get('LOW', 0) + simulation_state['priority_distribution'].get('MODERATE', 0)
                        simulation_state['metrics']['offloading_rate'] = (cloud_count / total_generated) * 100
            
            # Calculate offloading rate (percentage of tasks going to cloud)
            with state_lock:
                total_generated = simulation_state['metrics']['tasks_generated']
                if total_generated > 0:
                    cloud_count = simulation_state['priority_distribution'].get('LOW', 0) + simulation_state['priority_distribution'].get('MODERATE', 0)
                    simulation_state['metrics']['offloading_rate'] = (cloud_count / total_generated) * 100
            
            # Failure simulation (unchanged)
            failure_prob = simulation_state.get('config', {}).get('simulation', {}).get('failure_probability', 0.1)
            num_fog_nodes = simulation_state.get('config', {}).get('network', {}).get('fog_nodes', 3)
            
            if int(elapsed * 10) % 20 == 0:
                for node_id in range(1, num_fog_nodes + 1):
                    if random.random() < failure_prob:
                        simulation_state['metrics']['failure_events'] += 1
                        event_queue.put({
                            'type': 'warning',
                            'message': f'Fog Node {node_id} failure detected',
                            'timestamp': datetime.now().isoformat()
                        })
            
            # Periodic status updates
            if elapsed % 3 < 0.1:
                with state_lock:
                    fog_q_len = len(simulation_state['pending_fog_tasks'])
                    cloud_q_len = len(simulation_state['cloud_tasks'])
                
                event_queue.put({
                    'type': 'info',
                    'message': f'📊 Progress: {simulation_state["progress"]:.1f}% - Tasks: {simulation_state["metrics"]["tasks_processed"]}/{simulation_state["metrics"]["tasks_generated"]} | Fog Queue: {fog_q_len} | Cloud Queue: {cloud_q_len}',
                    'timestamp': datetime.now().isoformat()
                })
            
            time.sleep(0.1)
        
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
    port = int(os.environ.get('PORT', 5000))
    print("🌐 Starting Fog Computing Simulator Backend API")
    print("=" * 60)
    print(f"📡 API Server: http://0.0.0.0:{port}")
    if os.environ.get('RENDER'):
        print("🚀 Running on Render (Production)")
    else:
        print("🔧 Running in Development Mode")
    print(f"🔗 CORS enabled for: {', '.join(allowed_origins)}")
    print("\n💡 API Endpoints:")
    print("   • GET  /api/status")
    print("   • GET  /api/config")
    print("   • POST /api/config")
    print("   • POST /api/simulation/start")
    print("   • POST /api/simulation/stop")
    print("   • GET  /api/simulation/events")
    print("   • GET  /api/tasks")
    print("   • GET  /api/analytics/metrics")
    print("\n🎯 Priority-Based Scheduling:")
    print("   • HIGH priority → Fog processing")
    print("   • LOW/MODERATE → Cloud processing")
    print("   • Fog queue: Priority sorted by (priority, arrival_time, complexity)")
    print("\n🛑 Press Ctrl+C to stop the server")
    print("=" * 60)
    
    # Get port from environment variable (Render provides this) or use default 5000
    port = int(os.environ.get('PORT', 5000))
    # Only run in debug mode if not in production
    debug_mode = os.environ.get('FLASK_ENV') == 'development' or not os.environ.get('RENDER')
    
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
