import { initializeApp } from 'firebase/app'
import { getAuth } from 'firebase/auth'
import { getFirestore } from 'firebase/firestore'

const firebaseConfig = {
  apiKey: "AIzaSyAzi8DED5WbwVaGToSd5ZxMx4btP5oUcLY",
  authDomain: "swe-fog-latency-optimization.firebaseapp.com",
  projectId: "swe-fog-latency-optimization",
  storageBucket: "swe-fog-latency-optimization.firebasestorage.app",
  messagingSenderId: "702224469157",
  appId: "1:702224469157:web:d8530ce92499dd125d514c"
}

const app = initializeApp(firebaseConfig)
export const auth = getAuth(app)
export const db = getFirestore(app)


