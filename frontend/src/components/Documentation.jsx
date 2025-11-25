import React from 'react'

export default function Documentation() {
  return (
    <div className="space-y-6">
      <div className="mb-6 pb-4 border-b-2 border-gray-200">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Documentation</h1>
        <p className="text-gray-600">Comprehensive guide to the fog computing simulation platform</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <div className="lg:col-span-1">
          <div className="card sticky top-4">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Table of Contents</h3>
            <nav className="space-y-2">
              <a href="#getting-started" className="block text-sm text-gray-600 hover:text-primary">
                Getting Started
              </a>
              <a href="#simulation-basics" className="block text-sm text-gray-600 hover:text-primary">
                Simulation Basics
              </a>
              <a href="#configuration" className="block text-sm text-gray-600 hover:text-primary">
                Configuration
              </a>
              <a href="#advanced-features" className="block text-sm text-gray-600 hover:text-primary">
                Advanced Features
              </a>
              <a href="#api-reference" className="block text-sm text-gray-600 hover:text-primary">
                API Reference
              </a>
              <a href="#future-work" className="block text-sm text-gray-600 hover:text-primary">
                Future Work
              </a>
            </nav>
          </div>
        </div>

        <div className="lg:col-span-3 space-y-8">
          <section id="getting-started" className="card">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Getting Started</h2>
            <p className="text-gray-700 mb-4">
              Welcome to the Fog Computing Simulation Platform! This comprehensive tool allows you to
              simulate and analyze fog computing architectures with advanced features including node
              failure simulation, intelligent offloading, and real-time monitoring.
            </p>
            <h3 className="text-xl font-semibold text-gray-900 mb-3">Quick Start</h3>
            <ol className="list-decimal list-inside space-y-2 text-gray-700">
              <li>Configure your simulation parameters in the Configuration section</li>
              <li>Set up your network topology (fog nodes, IoT devices, cloud server)</li>
              <li>Configure task generation and offloading parameters</li>
              <li>Run the simulation and monitor results in real-time</li>
              <li>Analyze performance metrics and optimize your configuration</li>
            </ol>
          </section>

          <section id="simulation-basics" className="card">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Simulation Basics</h2>
            <p className="text-gray-700 mb-4">
              The simulation platform models a distributed fog computing environment with the following components:
            </p>
            <h3 className="text-xl font-semibold text-gray-900 mb-3">Core Components</h3>
            <ul className="list-disc list-inside space-y-2 text-gray-700">
              <li><strong>IoT Devices:</strong> Generate computational tasks with varying complexity</li>
              <li><strong>Fog Nodes:</strong> Process tasks locally or offload to cloud</li>
              <li><strong>Cloud Server:</strong> High-capacity processing for complex tasks</li>
              <li><strong>Network:</strong> Realistic latency modeling between components</li>
            </ul>
            <h3 className="text-xl font-semibold text-gray-900 mb-3 mt-4">Key Features</h3>
            <ul className="list-disc list-inside space-y-2 text-gray-700">
              <li>Dynamic task generation with configurable parameters</li>
              <li>Intelligent offloading decisions based on multiple factors</li>
              <li>Node failure simulation with automatic recovery</li>
              <li>Real-time performance monitoring and analytics</li>
            </ul>
          </section>

          <section id="advanced-features" className="card">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Advanced Features</h2>
            <p className="text-gray-700 mb-4">
              The platform includes several advanced features for comprehensive fog computing research:
            </p>
            <h3 className="text-xl font-semibold text-gray-900 mb-3">Node Failure Simulation</h3>
            <p className="text-gray-700 mb-4">
              Simulate realistic failure scenarios with configurable probability and duration. The system
              automatically handles task rerouting and recovery.
            </p>
            <h3 className="text-xl font-semibold text-gray-900 mb-3">Intelligent Offloading</h3>
            <p className="text-gray-700 mb-4">
              Advanced decision engine that considers task complexity, node utilization, deadlines, and
              network conditions to optimize task placement.
            </p>
            <h3 className="text-xl font-semibold text-gray-900 mb-3">Real-time Monitoring</h3>
            <p className="text-gray-700">
              Comprehensive monitoring of system performance, resource utilization, and failure events
              with detailed logging and analytics.
            </p>
          </section>

          <section id="future-work" className="card">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Future Work</h2>
            <p className="text-gray-700 mb-4">
              The platform is designed for continuous enhancement. Planned future features include:
            </p>
            <ul className="list-disc list-inside space-y-2 text-gray-700">
              <li><strong>Machine Learning Offloading:</strong> ML-based decision engines for adaptive optimization</li>
              <li><strong>Energy Modeling:</strong> Comprehensive energy consumption simulation</li>
              <li><strong>Device Mobility:</strong> Mobile IoT devices with handoff mechanisms</li>
              <li><strong>Enhanced Security:</strong> Encryption overhead and trust management</li>
              <li><strong>GUI Dashboard:</strong> Interactive visualization and configuration</li>
            </ul>
          </section>
        </div>
      </div>
    </div>
  )
}


