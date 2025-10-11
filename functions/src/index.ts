import * as functions from "firebase-functions";
import * as cors from "cors";
import * as admin from "firebase-admin";

// Initialize Firebase Admin SDK
admin.initializeApp();

// Initialize CORS middleware
// Note: In production, replace { origin: true } with your specific Vercel URL
// e.g., { origin: "https://your-app.vercel.app" }
const corsHandler = cors({ origin: true });

// Authentication middleware
const authenticateUser = async (req: any, res: any, next: any) => {
  try {
    const authHeader = req.headers.authorization;
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return res.status(401).json({ error: 'No valid authentication token provided' });
    }

    const token = authHeader.split('Bearer ')[1];
    const decodedToken = await admin.auth().verifyIdToken(token);
    req.user = decodedToken;
    next();
  } catch (error) {
    console.error('Authentication error:', error);
    return res.status(401).json({ error: 'Invalid authentication token' });
  }
};

/**
 * Cloud Function to process data packets on Fog nodes
 * Simulates fast local processing with minimal latency
 */
export const processOnFog = functions.https.onRequest((req, res) => {
  return corsHandler(req, res, async () => {
    try {
      // Authenticate user
      await authenticateUser(req, res, async () => {
        // Simulate fog processing delay (100ms)
        await new Promise(resolve => setTimeout(resolve, 100));
        
        res.status(200).json({
          message: "Packet processed by FOG",
          user: req.user.email
        });
      });
    } catch (error) {
      console.error("Error processing on fog:", error);
      res.status(500).json({
        error: "Failed to process packet on fog"
      });
    }
  });
});

/**
 * Cloud Function to process data packets on Cloud
 * Simulates slower cloud processing with higher latency
 */
export const processOnCloud = functions.https.onRequest((req, res) => {
  return corsHandler(req, res, async () => {
    try {
      // Authenticate user
      await authenticateUser(req, res, async () => {
        // Simulate cloud processing delay (500ms)
        await new Promise(resolve => setTimeout(resolve, 500));
        
        res.status(200).json({
          message: "Packet processed by CLOUD",
          user: req.user.email
        });
      });
    } catch (error) {
      console.error("Error processing on cloud:", error);
      res.status(500).json({
        error: "Failed to process packet on cloud"
      });
    }
  });
});
