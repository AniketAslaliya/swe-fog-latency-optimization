import { authService } from './auth';

/**
 * Data packet interface for the fog simulation
 */
export interface DataPacket {
  id: string;
  size: number;
  complexity: 'low' | 'high';
}

/**
 * API service for communicating with Firebase Cloud Functions
 */
class ApiService {
  private fogFunctionUrl: string;
  private cloudFunctionUrl: string;

  constructor() {
    // Get function URLs from environment variables
    this.fogFunctionUrl = import.meta.env.VITE_FOG_FUNCTION_URL;
    this.cloudFunctionUrl = import.meta.env.VITE_CLOUD_FUNCTION_URL;

    if (!this.fogFunctionUrl || !this.cloudFunctionUrl) {
      throw new Error('Missing required environment variables: VITE_FOG_FUNCTION_URL and VITE_CLOUD_FUNCTION_URL');
    }
  }

  /**
   * Get authenticated headers for API requests
   */
  private async getAuthHeaders(): Promise<HeadersInit> {
    const token = await authService.getIdToken();
    return {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    };
  }

  /**
   * Process a data packet on the fog node
   * @param packet - The data packet to process
   * @returns Promise with the processing result
   */
  async processOnFog(packet: DataPacket): Promise<{ message: string; user: string }> {
    const headers = await this.getAuthHeaders();
    const response = await fetch(this.fogFunctionUrl, {
      method: 'POST',
      headers,
      body: JSON.stringify(packet),
    });

    if (!response.ok) {
      throw new Error(`Fog processing failed: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Process a data packet on the cloud
   * @param packet - The data packet to process
   * @returns Promise with the processing result
   */
  async processOnCloud(packet: DataPacket): Promise<{ message: string; user: string }> {
    const headers = await this.getAuthHeaders();
    const response = await fetch(this.cloudFunctionUrl, {
      method: 'POST',
      headers,
      body: JSON.stringify(packet),
    });

    if (!response.ok) {
      throw new Error(`Cloud processing failed: ${response.statusText}`);
    }

    return response.json();
  }
}

// Export a singleton instance
export const apiService = new ApiService();
