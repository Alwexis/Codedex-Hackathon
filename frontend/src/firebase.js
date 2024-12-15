import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getAuth } from "firebase/auth";

//! Esta configuración está publica ya que el proyecto de Firebase es desechable y no contiene información sensible.
//! Además, se cambiará una vez la versión final de la aplicación esté lista.
const firebaseConfig = {
  apiKey: "AIzaSyByRec1mVaDvAXEQzgl8uosA_RzPnATmc4",
  authDomain: "wavenet-73cf7.firebaseapp.com",
  projectId: "wavenet-73cf7",
  storageBucket: "wavenet-73cf7.firebasestorage.app",
  messagingSenderId: "1011540918028",
  appId: "1:1011540918028:web:07fbcf0b772c9cced49329",
  measurementId: "G-RCVEKXC8J1"
};

// Initialize Firebase
export const app = initializeApp(firebaseConfig);
export const analytics = getAnalytics(app);
export const auth = getAuth(app);