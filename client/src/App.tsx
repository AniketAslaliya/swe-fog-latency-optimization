/*
  PROTOTYPE DEPLOYMENT GUIDE

  This project uses a decoupled architecture and requires two separate deployment steps.

  STEP 1: DEPLOY THE BACKEND (FIREBASE CLOUD FUNCTIONS)
  1. Open your terminal and navigate to the functions directory.
  2. Run the command: firebase deploy --only functions
  3. After deployment finishes, Firebase will provide you with the production URLs for your processOnFog and processOnCloud functions. Copy these URLs.

  STEP 2: CONFIGURE AND DEPLOY THE FRONTEND (VERCEL)
  1. Push your entire client folder to a new GitHub repository.
  2. Sign up for or log in to your Vercel account.
  3. On the Vercel dashboard, click "Add New... -> Project" and import your GitHub repository.
  4. In the "Configure Project" screen, expand the "Environment Variables" section.
  5. Add the following two variables, pasting the URLs you copied from Firebase:
     - Name: VITE_FOG_FUNCTION_URL, Value: [Your production fog function URL]
     - Name: VITE_CLOUD_FUNCTION_URL, Value: [Your production cloud function URL]
  6. Click "Deploy". Vercel will build and host your React application. The live site will now correctly communicate with your live Firebase backend.
*/

import React, { useState, useEffect } from 'react';
import { apiService, DataPacket } from './services/api';
import { authService, AuthUser } from './services/auth';
import './App.css';

interface LogMessage {
  id: string;
  timestamp: string;
  message: string;
  type: 'info' | 'success' | 'warning' | 'error';
}

function App() {
  const [logs, setLogs] = useState<LogMessage[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [user, setUser] = useState<AuthUser | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Initialize authentication state listener
  useEffect(() => {
    const unsubscribe = authService.onAuthStateChanged((user) => {
      setUser(user);
      setIsLoading(false);
    });

    return () => unsubscribe();
  }, []);

    const addLog = (message: string, type: LogMessage['type'] = 'info') => {
      const newLog: LogMessage = {
        id: Date.now().toString(),
        timestamp: new Date().toLocaleTimeString(),
        message,
        type,
      };
      setLogs(prev => [...prev, newLog]);
    };

  const handleGeneratePacket = async () => {
    if (isProcessing) return;
    
    setIsProcessing(true);
    
    try {
      // Create a new packet with random properties
      const newPacket: DataPacket = {
        id: `packet_${Date.now()}`,
        size: Math.floor(Math.random() * 1000), // 0-1000
        complexity: Math.random() < 0.5 ? 'low' : 'high'
      };

      addLog(`📦 Generated new packet: ID=${newPacket.id}, Size=${newPacket.size}, Complexity=${newPacket.complexity}`, 'info');

      // Record start time for latency calculation
      const startTime = performance.now();

      // Determine processing location based on offloading logic
      const shouldUseFog = newPacket.complexity === 'low' && newPacket.size < 500;
      const processingLocation = shouldUseFog ? 'FOG' : 'CLOUD';
      
      addLog(`🤔 Offloading decision: ${processingLocation} (${shouldUseFog ? 'Low complexity & small size' : 'High complexity or large size'})`, 'info');

      // Process the packet
      let result;
      if (shouldUseFog) {
        addLog(`🌫️ Sending packet to FOG node...`, 'info');
        result = await apiService.processOnFog(newPacket);
      } else {
        addLog(`☁️ Sending packet to CLOUD...`, 'info');
        result = await apiService.processOnCloud(newPacket);
      }

      // Calculate total latency
      const endTime = performance.now();
      const totalLatency = Math.round(endTime - startTime);

      addLog(`✅ ${result.message}`, 'success');
      addLog(`⏱️ Total round-trip latency: ${totalLatency}ms`, shouldUseFog ? 'success' : 'warning');

    } catch (error) {
      addLog(`❌ Error processing packet: ${error instanceof Error ? error.message : 'Unknown error'}`, 'error');
    } finally {
      setIsProcessing(false);
    }
  };

  const clearLogs = () => {
    setLogs([]);
  };

  const handleSignIn = async () => {
    try {
      await authService.signInWithGoogle();
      addLog('✅ Successfully signed in with Google', 'success');
    } catch (error) {
      addLog(`❌ Sign in failed: ${error instanceof Error ? error.message : 'Unknown error'}`, 'error');
    }
  };

  const handleSignOut = async () => {
    try {
      await authService.signOut();
      addLog('👋 Signed out successfully', 'info');
    } catch (error) {
      addLog(`❌ Sign out failed: ${error instanceof Error ? error.message : 'Unknown error'}`, 'error');
    }
  };

  if (isLoading) {
    return (
      <div className="app">
        <div className="container">
          <div className="loading">
            <h2>Loading...</h2>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <div className="container">
        <div className="header">
          <h1>Latency-Optimized Fog Architecture Simulator</h1>
          <div className="auth-section">
            {user ? (
              <div className="user-info">
                <img 
                  src={user.photoURL || '/default-avatar.png'} 
                  alt="User avatar" 
                  className="user-avatar"
                />
                <span className="user-name">{user.displayName || user.email}</span>
                <button onClick={handleSignOut} className="sign-out-button">
                  Sign Out
                </button>
              </div>
            ) : (
              <button onClick={handleSignIn} className="sign-in-button">
                Sign in with Google
              </button>
            )}
          </div>
        </div>
        
        {!user ? (
          <div className="auth-required">
            <h2>🔐 Authentication Required</h2>
            <p>Please sign in with Google to use the fog simulation.</p>
          </div>
        ) : (
          <>
            <div className="controls">
              <button 
                onClick={handleGeneratePacket} 
                disabled={isProcessing}
                className="generate-button"
              >
                {isProcessing ? 'Processing...' : 'Generate and Process Packet'}
              </button>
              
              {logs.length > 0 && (
                <button onClick={clearLogs} className="clear-button">
                  Clear Logs
                </button>
              )}
            </div>

            <div className="log-container">
              <h3>Event Log</h3>
              {logs.length === 0 ? (
                <p className="no-logs">No events yet. Click the button above to start the simulation!</p>
              ) : (
                <div className="logs">
                  {logs.map(log => (
                    <div key={log.id} className={`log-entry ${log.type}`}>
                      <span className="timestamp">[{log.timestamp}]</span>
                      <span className="message">{log.message}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default App;
