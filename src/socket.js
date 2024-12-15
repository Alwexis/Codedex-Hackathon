import { io } from "socket.io-client";

const SOCKET_URL = "https://codedex-hackathon.onrender.com/"; // Correcto
const socket = io(SOCKET_URL, {
  transports: ["websocket"], // Forzar WebSocket
  autoConnect: true,
  reconnectionAttempts: 5, // Intenta reconectar 5 veces
});

export default socket;
