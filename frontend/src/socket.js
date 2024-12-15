import { io } from "socket.io-client";

//? Habilitamos el autoConnect para que se conecte automáticamente al servidor y reconnectionAttempts para que intente reconectar al menos 5 veces
const SOCKET_URL = "https://codedex-hackathon.onrender.com/";
const socket = io(SOCKET_URL, {
  transports: ["websocket"], // Forzamos WebSocket
  autoConnect: true,
  reconnectionAttempts: 5, // Intenta reconectar 5 veces
});

export default socket;
