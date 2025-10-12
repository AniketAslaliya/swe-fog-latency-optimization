#!/usr/bin/env python3
"""
Test Web Interface
==================

Simple test script to verify the web interface is working correctly.
"""

import requests
import time
import json

def test_web_interface():
    """Test the web interface endpoints."""
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Fog Computing Simulator Web Interface")
    print("=" * 50)
    
    # Test 1: Check if server is running
    try:
        response = requests.get(f"{base_url}/api/status", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running")
            status = response.json()
            print(f"   Simulation running: {status['running']}")
            print(f"   Progress: {status['progress']}%")
        else:
            print(f"❌ Server returned status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to server: {e}")
        print("💡 Make sure the server is running on http://localhost:5000")
        return False
    
    # Test 2: Get configuration
    try:
        response = requests.get(f"{base_url}/api/config")
        if response.status_code == 200:
            print("✅ Configuration endpoint working")
            config = response.json()
            print(f"   Fog nodes: {config['network']['fog_nodes']}")
            print(f"   IoT devices: {config['network']['iot_devices']}")
        else:
            print(f"❌ Configuration endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
    
    # Test 3: Get network topology
    try:
        response = requests.get(f"{base_url}/api/network/topology")
        if response.status_code == 200:
            print("✅ Network topology endpoint working")
            topology = response.json()
            print(f"   Cloud server: {topology['cloud_server']['id']}")
            print(f"   Fog nodes: {len(topology['fog_nodes'])}")
            print(f"   IoT devices: {len(topology['iot_devices'])}")
        else:
            print(f"❌ Topology endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Topology test failed: {e}")
    
    # Test 4: Get analytics
    try:
        response = requests.get(f"{base_url}/api/analytics/metrics")
        if response.status_code == 200:
            print("✅ Analytics endpoint working")
            analytics = response.json()
            print(f"   Performance summary available: {len(analytics['performance_summary'])} metrics")
        else:
            print(f"❌ Analytics endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Analytics test failed: {e}")
    
    # Test 5: Test simulation start/stop
    try:
        # Start simulation
        response = requests.post(f"{base_url}/api/simulation/start", 
                               json={"duration": 10}, timeout=5)
        if response.status_code == 200:
            print("✅ Simulation start endpoint working")
            
            # Wait a bit
            time.sleep(2)
            
            # Check status
            response = requests.get(f"{base_url}/api/status")
            if response.status_code == 200:
                status = response.json()
                print(f"   Simulation running: {status['running']}")
                print(f"   Progress: {status['progress']}%")
            
            # Stop simulation
            response = requests.post(f"{base_url}/api/simulation/stop")
            if response.status_code == 200:
                print("✅ Simulation stop endpoint working")
        else:
            print(f"❌ Simulation start failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Simulation test failed: {e}")
    
    print("\n🎉 Web interface testing completed!")
    print("🌐 Open http://localhost:5000 in your browser to use the interface")
    return True

if __name__ == "__main__":
    test_web_interface()
