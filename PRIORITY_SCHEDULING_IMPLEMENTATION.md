# Priority-Based Scheduling Implementation

## 📋 Overview

This document describes the implementation of priority-based task scheduling and routing for IoT devices in the Fog Computing Simulator.

## 🎯 Scheduling Rules

### Task Routing
1. **HIGH Priority** → Always processed on **Fog**
2. **LOW/MODERATE Priority** → Always offloaded to **Cloud**

### Fog Queue Scheduling (for HIGH priority tasks)
When multiple HIGH priority tasks are in the fog queue, they are scheduled based on:
1. **Priority weight** (highest first) - HIGH = 3, MODERATE = 2, LOW = 1
2. **Earliest arrival_time** (if priority tie)
3. **Lower complexity** (if arrival_time tie)

Sort key: `(-priority_weight, arrival_time, complexity)`

## 🔧 Backend Changes (app.py)

### 1. New Data Structures

```python
# Priority queue for fog tasks (heap-based)
'pending_fog_tasks': []  # Heap with sort_key tuples

# Regular queue for cloud tasks
'cloud_tasks': []  # FIFO list

# Track active tasks
'active_tasks': {}  # Dict by task_id

# Priority distribution counter
'priority_distribution': {'HIGH': 0, 'MODERATE': 0, 'LOW': 0}
```

### 2. New Functions

- **`generate_task(current_time)`**: Creates tasks with priority, complexity, arrival_time
- **`schedule_fog_task(task)`**: Adds HIGH priority tasks to fog priority queue
- **`schedule_cloud_task(task)`**: Adds LOW/MODERATE tasks to cloud queue
- **`process_fog_task(current_time)`**: Processes highest priority fog task
- **`process_cloud_task(current_time)`**: Processes cloud task (FIFO)

### 3. Updated Simulation Loop

The `run_simulation_background()` function now:
- Generates tasks every 0.5 seconds with random priority
- Routes HIGH → fog queue, LOW/MODERATE → cloud queue
- Processes fog tasks using priority queue (highest first)
- Processes cloud tasks using FIFO
- Tracks latency separately for fog and cloud
- Updates priority distribution counters

### 4. Enhanced API Endpoints

#### `/api/status`
Now returns:
- `fog_queue_length`: Number of tasks in fog queue
- `cloud_queue_length`: Number of tasks in cloud queue
- `priority_distribution`: Count of each priority level

#### `/api/analytics/metrics`
Now includes:
- `priority_distribution`: {HIGH: x, MODERATE: y, LOW: z}
- `fog_queue_length`: Current fog queue size
- `cloud_queue_length`: Current cloud queue size

#### `/api/tasks` (NEW)
Returns current task queues:
- `fog_queue`: Array of tasks in fog priority queue
- `cloud_queue`: Array of tasks in cloud queue
- `active_tasks`: Array of currently processing tasks

#### `/api/network/topology`
Now includes `queued_tasks` count for each fog node

### 5. Event Logging

Events now include:
- "Task X generated: HIGH (complexity=450)"
- "Task X assigned to fog"
- "Task X offloaded to cloud"
- "Fog scheduling: Task 7 processed before Task 9 (higher priority)"

## 🎨 Frontend Changes

### 1. New Component: TaskQueue.jsx

Displays a table showing:
- Task ID
- Priority (with colored badges: RED=HIGH, ORANGE=MODERATE, GREEN=LOW)
- Complexity
- Assigned To (FOG/CLOUD)
- Arrival Time
- Status (Fog Queue / Cloud Queue / Processing)

### 2. Updated Dashboard.jsx

**New Stats Cards:**
- Fog Queue Length
- Cloud Queue Length
- HIGH Priority Tasks Count

**New Task Queue Section:**
- Full task table with all task details
- Real-time updates every 2 seconds

**Updated Network Topology:**
- Shows number of queued tasks per fog node
- Displays task count below each fog node

### 3. Updated Analytics.jsx

**New Priority Distribution Chart:**
- Doughnut chart showing HIGH/MODERATE/LOW distribution
- Colors: Red (HIGH), Orange (MODERATE), Green (LOW)

**Enhanced Performance Summary:**
- Fog Queue Length
- Cloud Queue Length
- Total HIGH Priority Tasks

**Updated Task Distribution Chart:**
- Labels now show "Fog Processing (HIGH)" and "Cloud Processing (LOW/MOD)"

### 4. Updated useSimulation Hook

Now tracks:
- `fog_queue_length`
- `cloud_queue_length`
- `priority_distribution`

## 📊 Task Generation

### Priority Distribution
- **30%** HIGH priority
- **40%** MODERATE priority
- **30%** LOW priority

### Complexity Range
Based on config: `tasks.complexity_range` (default: 50-2000)

### Generation Rate
Tasks generated every **0.5 seconds** during simulation

## 🔄 Processing Flow

```
IoT Device
    ↓
Generate Task (priority, complexity, arrival_time)
    ↓
    ├─ HIGH Priority → schedule_fog_task() → Fog Priority Queue
    └─ LOW/MODERATE → schedule_cloud_task() → Cloud Queue
    ↓
    ├─ Fog: process_fog_task() → Priority Queue Pop (highest first)
    └─ Cloud: process_cloud_task() → FIFO Pop
    ↓
Calculate Latency (fog ~30-50ms, cloud ~120-150ms)
    ↓
Update Metrics & Events
```

## 🎨 UI Features

### Priority Badges
- **HIGH**: Red badge (`bg-red-100 text-red-700`)
- **MODERATE**: Orange badge (`bg-orange-100 text-orange-700`)
- **LOW**: Green badge (`bg-green-100 text-green-700`)

### Queue Indicators
- Fog Queue: Indigo color
- Cloud Queue: Purple color
- Active Tasks: Blue color

### Topology Visualization
- Fog nodes show task count below node label
- Task count distributed evenly across fog nodes

## 📈 Metrics & Analytics

### Real-time Metrics
- Task generation rate
- Processing rate (fog vs cloud)
- Queue lengths (fog and cloud)
- Priority distribution
- Average latency (separate for fog and cloud)

### Charts
1. **Priority Distribution**: Doughnut chart
2. **Latency Comparison**: Line chart (fog vs cloud)
3. **Task Distribution**: Doughnut chart (fog/cloud/failed)
4. **Resource Utilization**: Bar chart
5. **Failure Events**: Bar chart

## 🔒 Thread Safety

All queue operations use `threading.Lock()` via `state_lock` to ensure thread-safe access to shared state.

## 🧪 Testing

To test the implementation:

1. Start simulation
2. Observe task generation in Dashboard → Task Queue
3. Check priority distribution in Analytics
4. Verify HIGH tasks go to fog, LOW/MODERATE to cloud
5. Monitor queue lengths in real-time
6. Check event logs for scheduling decisions

## 📝 Summary

The implementation successfully adds:
✅ Priority-based task generation (HIGH/MODERATE/LOW)
✅ Intelligent routing (HIGH→fog, LOW/MODERATE→cloud)
✅ Priority queue scheduling for fog (by priority, arrival_time, complexity)
✅ Real-time task queue visualization
✅ Priority distribution analytics
✅ Enhanced event logging
✅ Thread-safe operations

All changes maintain backward compatibility with existing features while adding the new priority-based scheduling system.


