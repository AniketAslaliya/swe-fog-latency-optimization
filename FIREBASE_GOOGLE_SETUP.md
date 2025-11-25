# 🔧 Fixing Google Sign-In Authentication Error

If you're seeing `Firebase: Error (auth/internal-error)` when trying to sign in with Google, follow these steps:

## ✅ Quick Fix: Use Guest Mode

The app now supports **Guest Mode** - you can use it without signing in! Just click "Continue as Guest" on the login page.

## 🔐 Setting Up Google Sign-In (Optional)

If you want to enable Google Sign-In, you need to configure it in Firebase Console:

### Step 1: Enable Google Sign-In Provider

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select your project: `swe-fog-latency-optimization`
3. Navigate to **Authentication** > **Sign-in method**
4. Click on **Google** provider
5. Toggle **Enable** to ON
6. Enter your **Support email** (your email address)
7. Click **Save**

### Step 2: Configure OAuth Consent Screen (If Required)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project: `swe-fog-latency-optimization`
3. Navigate to **APIs & Services** > **OAuth consent screen**
4. Choose **External** (unless you have a Google Workspace)
5. Fill in required fields:
   - App name: `Fog Computing Simulator`
   - User support email: Your email
   - Developer contact: Your email
6. Click **Save and Continue**
7. Add scopes (if needed): `email`, `profile`, `openid`
8. Add test users (if in testing mode)
9. Click **Save and Continue**

### Step 3: Add Authorized Domains

1. In Firebase Console, go to **Authentication** > **Settings** > **Authorized domains**
2. Make sure these are added:
   - `localhost`
   - `127.0.0.1`
   - Your custom domain (if any)

### Step 4: Verify Configuration

1. Make sure your Firebase project has billing enabled (if required)
2. Check that the OAuth client is created automatically in Google Cloud Console
3. Try signing in with Google again

## 🚨 Common Issues

### Issue: "auth/internal-error"
**Solution**: Google Sign-In provider is not enabled in Firebase Console

### Issue: "auth/operation-not-allowed"
**Solution**: Enable Google Sign-In in Firebase Console > Authentication > Sign-in method

### Issue: "auth/popup-blocked"
**Solution**: Allow popups in your browser settings for localhost:3000

### Issue: OAuth consent screen not configured
**Solution**: Complete the OAuth consent screen setup in Google Cloud Console

## 💡 Alternative: Use Email/Password Authentication

You can always use email/password authentication instead:
1. Click "Sign Up" tab
2. Enter your email and password
3. Create an account
4. Sign in with email/password

## 📝 Note

The app works perfectly fine in **Guest Mode** without any authentication. Google Sign-In is optional and only needed if you want to:
- Save your simulation data to Firebase
- Access your data from multiple devices
- Use cloud-based device management

