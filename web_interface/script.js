/**
 * Fog Computing Simulator - Web Interface
 * Advanced platform for fog computing research and analysis
 */

class FogSimulatorApp {
    constructor() {
        this.currentSection = 'dashboard';
        this.simulationRunning = false;
        this.simulationData = {
            fogNodes: 3,
            iotDevices: 10,
            tasksProcessed: 0,
            avgLatency: 0,
            failureEvents: [],
            performanceMetrics: {}
        };
        this.charts = {};
        this.config = {};
        this.apiBaseUrl = 'http://localhost:5000/api';
        this.eventInterval = null;
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadConfiguration();
        this.initializeCharts();
        this.updateDashboard();
    }

    setupEventListeners() {
        // Navigation
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const section = link.dataset.section;
                this.showSection(section);
            });
        });

        // Simulation controls
        document.getElementById('runSimulation').addEventListener('click', () => {
            this.runSimulation();
        });

        // Configuration tabs
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const tab = btn.dataset.tab;
                this.showConfigTab(tab);
            });
        });

        // Configuration actions
        document.getElementById('saveConfig').addEventListener('click', () => {
            this.saveConfiguration();
        });

        document.getElementById('loadConfig').addEventListener('click', () => {
            this.loadConfiguration();
        });

        document.getElementById('resetConfig').addEventListener('click', () => {
            this.resetConfiguration();
        });

        // Failure probability slider
        const failureSlider = document.getElementById('failureProbability');
        const failureValue = document.getElementById('failureProbValue');
        failureSlider.addEventListener('input', (e) => {
            failureValue.textContent = e.target.value;
        });

        // Activity controls
        document.getElementById('clearActivity').addEventListener('click', () => {
            this.clearActivity();
        });

        // Topology refresh
        document.getElementById('refreshTopology').addEventListener('click', () => {
            this.refreshTopology();
        });
    }

    showSection(section) {
        // Update navigation
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
        });
        document.querySelector(`[data-section="${section}"]`).classList.add('active');

        // Update content
        document.querySelectorAll('.content-section').forEach(sec => {
            sec.classList.remove('active');
        });
        document.getElementById(section).classList.add('active');

        this.currentSection = section;

        // Update section-specific content
        if (section === 'dashboard') {
            this.updateDashboard();
        } else if (section === 'analytics') {
            this.updateAnalytics();
        }
    }

    showConfigTab(tab) {
        // Update tab buttons
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-tab="${tab}"]`).classList.add('active');

        // Update tab content
        document.querySelectorAll('.tab-panel').forEach(panel => {
            panel.classList.remove('active');
        });
        document.getElementById(`${tab}-tab`).classList.add('active');
    }

    async loadConfiguration() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/config`);
            if (response.ok) {
                this.config = await response.json();
                this.updateConfigurationUI();
                this.addActivity('Configuration loaded from server');
            } else {
                throw new Error('Failed to load configuration');
            }
        } catch (error) {
            console.error('Error loading configuration:', error);
            // Load default configuration as fallback
            this.config = {
                simulation: {
                    duration: 100,
                    enable_failures: true,
                    failure_probability: 0.1
                },
                network: {
                    fog_nodes: 3,
                    iot_devices: 10
                },
                tasks: {
                    rate_range: [0.1, 0.3],
                    complexity_range: [50, 2000]
                },
                latency: {
                    base_latency: 0.01,
                    cloud_latency: 5.0
                },
                offloading: {
                    complexity_threshold: 1000,
                    utilization_threshold: 0.8
                }
            };
            this.updateConfigurationUI();
            this.addActivity('Configuration loaded (default)');
        }
    }

    updateConfigurationUI() {
        // Update form fields with current configuration
        document.getElementById('simulationDuration').value = this.config.simulation?.duration || 100;
        document.getElementById('enableFailures').checked = this.config.simulation?.enable_failures || true;
        document.getElementById('failureProbability').value = this.config.simulation?.failure_probability || 0.1;
        document.getElementById('failureProbValue').textContent = this.config.simulation?.failure_probability || 0.1;

        document.getElementById('numFogNodes').value = this.config.network?.fog_nodes || 3;
        document.getElementById('numIoTDevices').value = this.config.network?.iot_devices || 10;
        document.getElementById('cloudCPU').value = 10000;
        document.getElementById('cloudMemory').value = 32000;

        document.getElementById('taskRateMin').value = this.config.tasks?.rate_range?.[0] || 0.1;
        document.getElementById('taskRateMax').value = this.config.tasks?.rate_range?.[1] || 0.3;
        document.getElementById('complexityMin').value = this.config.tasks?.complexity_range?.[0] || 50;
        document.getElementById('complexityMax').value = this.config.tasks?.complexity_range?.[1] || 2000;

        document.getElementById('baseLatency').value = this.config.latency?.base_latency || 0.01;
        document.getElementById('cloudLatency').value = this.config.latency?.cloud_latency || 5.0;
        document.getElementById('fogToCloudMultiplier').value = 0.02;

        document.getElementById('complexityThreshold').value = this.config.offloading?.complexity_threshold || 1000;
        document.getElementById('utilizationThreshold').value = this.config.offloading?.utilization_threshold || 0.8;
        document.getElementById('deadlineThreshold').value = 5.0;
        document.getElementById('queueThreshold').value = 5;
    }

    async saveConfiguration() {
        try {
            // Collect configuration from form
            const configData = {
                simulation: {
                    duration: parseInt(document.getElementById('simulationDuration').value),
                    enable_failures: document.getElementById('enableFailures').checked,
                    failure_probability: parseFloat(document.getElementById('failureProbability').value)
                },
                network: {
                    fog_nodes: parseInt(document.getElementById('numFogNodes').value),
                    iot_devices: parseInt(document.getElementById('numIoTDevices').value)
                },
                tasks: {
                    rate_range: [
                        parseFloat(document.getElementById('taskRateMin').value),
                        parseFloat(document.getElementById('taskRateMax').value)
                    ],
                    complexity_range: [
                        parseInt(document.getElementById('complexityMin').value),
                        parseInt(document.getElementById('complexityMax').value)
                    ]
                },
                latency: {
                    base_latency: parseFloat(document.getElementById('baseLatency').value),
                    cloud_latency: parseFloat(document.getElementById('cloudLatency').value)
                },
                offloading: {
                    complexity_threshold: parseInt(document.getElementById('complexityThreshold').value),
                    utilization_threshold: parseFloat(document.getElementById('utilizationThreshold').value)
                }
            };

            const response = await fetch(`${this.apiBaseUrl}/config`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(configData)
            });

            if (response.ok) {
                this.config = configData;
                this.addActivity('Configuration saved to server');
                this.showNotification('Configuration saved!', 'success');
            } else {
                throw new Error('Failed to save configuration');
            }
        } catch (error) {
            console.error('Error saving configuration:', error);
            this.showNotification('Failed to save configuration', 'error');
        }
    }

    resetConfiguration() {
        this.loadConfiguration();
        this.addActivity('Configuration reset to defaults');
        this.showNotification('Configuration reset!', 'info');
    }

    async runSimulation() {
        if (this.simulationRunning) {
            await this.stopSimulation();
            return;
        }

        try {
            const duration = parseInt(document.getElementById('simulationDuration').value);
            
            const response = await fetch(`${this.apiBaseUrl}/simulation/start`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ duration })
            });

            if (response.ok) {
                this.simulationRunning = true;
                this.updateSimulationStatus('Running', 'running');
                this.addActivity('Simulation started');

                // Update run button
                const runBtn = document.getElementById('runSimulation');
                runBtn.innerHTML = '<i class="fas fa-stop"></i> Stop Simulation';
                runBtn.classList.add('btn-danger');

                // Start event polling
                this.startEventPolling();
            } else {
                throw new Error('Failed to start simulation');
            }
        } catch (error) {
            console.error('Error starting simulation:', error);
            this.showNotification('Failed to start simulation', 'error');
        }
    }

    async stopSimulation() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/simulation/stop`, {
                method: 'POST'
            });

            if (response.ok) {
                this.simulationRunning = false;
                this.updateSimulationStatus('Stopped', 'stopped');
                this.addActivity('Simulation stopped');

                // Update run button
                const runBtn = document.getElementById('runSimulation');
                runBtn.innerHTML = '<i class="fas fa-play"></i> Run Simulation';
                runBtn.classList.remove('btn-danger');

                // Stop event polling
                this.stopEventPolling();

                // Update final metrics
                this.updateSimulationMetrics();
            } else {
                throw new Error('Failed to stop simulation');
            }
        } catch (error) {
            console.error('Error stopping simulation:', error);
            this.showNotification('Failed to stop simulation', 'error');
        }
    }

    simulateProgress() {
        if (!this.simulationRunning) return;

        const duration = this.config.simulation.duration;
        const startTime = Date.now();
        const endTime = startTime + (duration * 1000);

        const updateProgress = () => {
            if (!this.simulationRunning) return;

            const now = Date.now();
            const elapsed = (now - startTime) / 1000;
            const progress = Math.min((elapsed / duration) * 100, 100);

            // Update progress bar
            document.getElementById('simulationProgress').style.width = `${progress}%`;

            // Update metrics
            document.getElementById('elapsedTime').textContent = `${elapsed.toFixed(1)}s`;
            document.getElementById('tasksGenerated').textContent = Math.floor(elapsed * 2.5);
            document.getElementById('tasksProcessedSim').textContent = Math.floor(elapsed * 2.3);

            // Simulate random events
            if (Math.random() < 0.1) {
                this.simulateRandomEvent();
            }

            if (progress >= 100) {
                this.completeSimulation();
            } else {
                setTimeout(updateProgress, 100);
            }
        };

        updateProgress();
    }

    simulateRandomEvent() {
        const events = [
            'Task generated by IoT device',
            'Task processed on fog node',
            'Task offloaded to cloud',
            'Node failure detected',
            'Node recovery completed',
            'Network latency measured'
        ];

        const event = events[Math.floor(Math.random() * events.length)];
        this.addActivity(event);
    }

    completeSimulation() {
        this.simulationRunning = false;
        this.updateSimulationStatus('Completed', 'completed');
        this.addActivity('Simulation completed successfully');

        // Update final metrics
        this.simulationData.tasksProcessed = Math.floor(this.config.simulation.duration * 2.3);
        this.simulationData.avgLatency = Math.random() * 100 + 50;

        // Update run button
        const runBtn = document.getElementById('runSimulation');
        runBtn.innerHTML = '<i class="fas fa-play"></i> Run Simulation';
        runBtn.classList.remove('btn-danger');

        // Update analytics
        this.updateAnalytics();
        this.showNotification('Simulation completed!', 'success');
    }

    updateSimulationStatus(status, type) {
        const statusIndicator = document.getElementById('simulationStatus');
        const statusDot = statusIndicator.querySelector('.status-dot');
        const statusText = statusIndicator.querySelector('span');

        statusText.textContent = status;
        statusDot.className = 'status-dot';

        switch (type) {
            case 'running':
                statusDot.style.background = '#4299e1';
                break;
            case 'stopped':
                statusDot.style.background = '#ed8936';
                break;
            case 'completed':
                statusDot.style.background = '#48bb78';
                break;
            default:
                statusDot.style.background = '#48bb78';
        }
    }

    startEventPolling() {
        this.eventInterval = setInterval(async () => {
            await this.pollSimulationEvents();
            await this.updateSimulationStatus();
        }, 1000);
    }

    stopEventPolling() {
        if (this.eventInterval) {
            clearInterval(this.eventInterval);
            this.eventInterval = null;
        }
    }

    async pollSimulationEvents() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/simulation/events`);
            if (response.ok) {
                const data = await response.json();
                data.events.forEach(event => {
                    this.addActivity(event.message);
                });
            }
        } catch (error) {
            console.error('Error polling events:', error);
        }
    }

    async updateSimulationStatus() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/status`);
            if (response.ok) {
                const status = await response.json();
                
                // Update progress bar
                document.getElementById('simulationProgress').style.width = `${status.progress}%`;
                
                // Update metrics
                document.getElementById('elapsedTime').textContent = `${(status.progress * this.config.simulation.duration / 100).toFixed(1)}s`;
                document.getElementById('tasksGenerated').textContent = status.metrics.tasks_generated;
                document.getElementById('tasksProcessedSim').textContent = status.metrics.tasks_processed;
                
                // Update dashboard stats
                document.getElementById('tasksProcessed').textContent = status.metrics.tasks_processed;
                document.getElementById('avgLatency').textContent = `${status.metrics.avg_latency.toFixed(1)}ms`;
                
                // Check if simulation completed
                if (status.progress >= 100 && this.simulationRunning) {
                    this.simulationRunning = false;
                    this.updateSimulationStatus('Completed', 'completed');
                    this.addActivity('Simulation completed successfully');
                    
                    const runBtn = document.getElementById('runSimulation');
                    runBtn.innerHTML = '<i class="fas fa-play"></i> Run Simulation';
                    runBtn.classList.remove('btn-danger');
                    
                    this.stopEventPolling();
                    this.updateAnalytics();
                    this.showNotification('Simulation completed!', 'success');
                }
            }
        } catch (error) {
            console.error('Error updating status:', error);
        }
    }

    updateSimulationMetrics() {
        document.getElementById('tasksProcessed').textContent = this.simulationData.tasksProcessed;
        document.getElementById('avgLatency').textContent = `${this.simulationData.avgLatency.toFixed(1)}ms`;
    }

    updateDashboard() {
        // Update stats
        document.getElementById('fogNodesCount').textContent = this.config.network?.fog_nodes || 3;
        document.getElementById('iotDevicesCount').textContent = this.config.network?.iot_devices || 10;
        document.getElementById('tasksProcessed').textContent = this.simulationData.tasksProcessed;
        document.getElementById('avgLatency').textContent = `${this.simulationData.avgLatency.toFixed(1)}ms`;

        // Update topology visualization
        this.updateTopologyVisualization();
    }

    updateTopologyVisualization() {
        const canvas = document.getElementById('topologyCanvas');
        canvas.innerHTML = `
            <div class="topology-placeholder">
                <i class="fas fa-network-wired" style="font-size: 3rem; color: #667eea; margin-bottom: 1rem;"></i>
                <h3>Network Topology</h3>
                <p>Fog Nodes: ${this.config.network?.fog_nodes || 3} | IoT Devices: ${this.config.network?.iot_devices || 10}</p>
                <p>Click "Refresh" to update visualization</p>
            </div>
        `;
    }

    refreshTopology() {
        this.addActivity('Network topology refreshed');
        this.updateTopologyVisualization();
    }

    async updateAnalytics() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/analytics/metrics`);
            if (response.ok) {
                const analytics = await response.json();
                
                // Update performance summary
                document.getElementById('avgResponseTime').textContent = analytics.performance_summary.avg_response_time;
                document.getElementById('successRate').textContent = analytics.performance_summary.success_rate;
                document.getElementById('offloadingRate').textContent = analytics.performance_summary.offloading_rate;
                document.getElementById('energyEfficiency').textContent = analytics.performance_summary.energy_efficiency;

                // Update charts with real data
                this.updateChartsWithData(analytics);
            }
        } catch (error) {
            console.error('Error updating analytics:', error);
            // Fallback to random data
            document.getElementById('avgResponseTime').textContent = `${(Math.random() * 200 + 100).toFixed(1)}ms`;
            document.getElementById('successRate').textContent = `${(Math.random() * 10 + 90).toFixed(1)}%`;
            document.getElementById('offloadingRate').textContent = `${(Math.random() * 30 + 10).toFixed(1)}%`;
            document.getElementById('energyEfficiency').textContent = 'N/A';
        }
    }

    initializeCharts() {
        // Initialize Chart.js charts
        this.charts.latency = this.createLatencyChart();
        this.charts.distribution = this.createDistributionChart();
        this.charts.utilization = this.createUtilizationChart();
        this.charts.failure = this.createFailureChart();
    }

    createLatencyChart() {
        const ctx = document.getElementById('latencyChart').getContext('2d');
        return new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['0s', '20s', '40s', '60s', '80s', '100s'],
                datasets: [{
                    label: 'Fog Processing',
                    data: [45, 52, 48, 55, 50, 47],
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    tension: 0.4
                }, {
                    label: 'Cloud Processing',
                    data: [120, 125, 130, 128, 132, 129],
                    borderColor: '#764ba2',
                    backgroundColor: 'rgba(118, 75, 162, 0.1)',
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Latency (ms)'
                        }
                    }
                }
            }
        });
    }

    createDistributionChart() {
        const ctx = document.getElementById('distributionChart').getContext('2d');
        return new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Fog Processing', 'Cloud Processing', 'Failed'],
                datasets: [{
                    data: [65, 30, 5],
                    backgroundColor: ['#667eea', '#764ba2', '#f56565'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                    }
                }
            }
        });
    }

    createUtilizationChart() {
        const ctx = document.getElementById('utilizationChart').getContext('2d');
        return new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Fog Node 1', 'Fog Node 2', 'Fog Node 3', 'Cloud Server'],
                datasets: [{
                    label: 'CPU Utilization (%)',
                    data: [75, 82, 68, 45],
                    backgroundColor: ['#667eea', '#764ba2', '#f093fb', '#48bb78'],
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        title: {
                            display: true,
                            text: 'Utilization (%)'
                        }
                    }
                }
            }
        });
    }

    createFailureChart() {
        const ctx = document.getElementById('failureChart').getContext('2d');
        return new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Node 1', 'Node 2', 'Node 3'],
                datasets: [{
                    label: 'Failure Events',
                    data: [2, 1, 3],
                    backgroundColor: '#f56565',
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Failure Count'
                        }
                    }
                }
            }
        });
    }

    updateChartsWithData(analytics) {
        // Update charts with real analytics data
        if (this.charts.latency && analytics.latency_data) {
            this.charts.latency.data.datasets[0].data = analytics.latency_data.fog_processing;
            this.charts.latency.data.datasets[1].data = analytics.latency_data.cloud_processing;
            this.charts.latency.data.labels = analytics.latency_data.timestamps;
            this.charts.latency.update();
        }

        if (this.charts.distribution && analytics.task_distribution) {
            this.charts.distribution.data.datasets[0].data = [
                analytics.task_distribution.fog_processing,
                analytics.task_distribution.cloud_processing,
                analytics.task_distribution.failed
            ];
            this.charts.distribution.update();
        }

        if (this.charts.utilization && analytics.resource_utilization) {
            const utilizationData = [...analytics.resource_utilization.fog_nodes, analytics.resource_utilization.cloud_server];
            this.charts.utilization.data.datasets[0].data = utilizationData;
            this.charts.utilization.update();
        }

        if (this.charts.failure && analytics.failure_events) {
            this.charts.failure.data.datasets[0].data = [
                analytics.failure_events.node_1,
                analytics.failure_events.node_2,
                analytics.failure_events.node_3
            ];
            this.charts.failure.update();
        }
    }

    updateCharts() {
        // Fallback method for updating charts with random data
        if (this.charts.latency) {
            const newData = Array.from({length: 6}, () => Math.random() * 100 + 50);
            this.charts.latency.data.datasets[0].data = newData;
            this.charts.latency.update();
        }

        if (this.charts.distribution) {
            const fogPercent = Math.random() * 20 + 60;
            const cloudPercent = Math.random() * 20 + 20;
            const failedPercent = 100 - fogPercent - cloudPercent;
            
            this.charts.distribution.data.datasets[0].data = [fogPercent, cloudPercent, failedPercent];
            this.charts.distribution.update();
        }

        if (this.charts.utilization) {
            const newUtilization = Array.from({length: 4}, () => Math.random() * 40 + 30);
            this.charts.utilization.data.datasets[0].data = newUtilization;
            this.charts.utilization.update();
        }
    }

    addActivity(message) {
        const activityLog = document.getElementById('activityLog');
        const timestamp = new Date().toLocaleTimeString();
        
        const activityItem = document.createElement('div');
        activityItem.className = 'activity-item';
        activityItem.innerHTML = `
            <div class="activity-icon">
                <i class="fas fa-info-circle"></i>
            </div>
            <div class="activity-content">
                <p>${message}</p>
                <span class="activity-time">${timestamp}</span>
            </div>
        `;
        
        activityLog.insertBefore(activityItem, activityLog.firstChild);
        
        // Keep only last 10 activities
        while (activityLog.children.length > 10) {
            activityLog.removeChild(activityLog.lastChild);
        }
    }

    clearActivity() {
        const activityLog = document.getElementById('activityLog');
        activityLog.innerHTML = `
            <div class="activity-item">
                <div class="activity-icon">
                    <i class="fas fa-info-circle"></i>
                </div>
                <div class="activity-content">
                    <p>Activity log cleared</p>
                    <span class="activity-time">Just now</span>
                </div>
            </div>
        `;
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
            <span>${message}</span>
        `;
        
        // Add styles
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === 'success' ? '#48bb78' : type === 'error' ? '#f56565' : '#4299e1'};
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            z-index: 10000;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-weight: 500;
            animation: slideIn 0.3s ease;
        `;
        
        document.body.appendChild(notification);
        
        // Remove after 3 seconds
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
    
    .topology-placeholder {
        text-align: center;
        color: #718096;
    }
    
    .topology-placeholder h3 {
        margin: 1rem 0 0.5rem 0;
        color: #2d3748;
    }
    
    .topology-placeholder p {
        margin: 0.5rem 0;
        font-size: 0.9rem;
    }
`;
document.head.appendChild(style);

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    window.fogSimulator = new FogSimulatorApp();
});
