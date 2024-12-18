import React, { createContext, useState, useEffect, useContext } from 'react';
import { onAuthStateChanged } from 'firebase/auth';
import { auth } from "../firebase";
import { useNavigate, useLocation } from 'react-router-dom';  // Asegúrate de importar useLocation

// Crear un contexto
const AuthContext = createContext();

// Proveedor de contexto para envolver la aplicación
export const AuthProvider = ({ children }) => {
    const navigate = useNavigate();
    const location = useLocation();  // Usamos useLocation para obtener la ubicación actual
    const [user, setUser] = useState(null);
    const [firebaseUser, setFirebaseUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const [userLikes, setUserLikes] = useState(0);
    const [chats, setChats] = useState([]);

    const getChats = async (accessToken) => {
        if (!accessToken) return;
        const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/chats`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${accessToken}`,
            }
        });
        const r = await response.json();
        if (r.status === "success") {
            setChats(JSON.parse(r.result));
        } else {
            setChats([]);
        }
    };

    const getUserLikes = async (accessToken) => {
        const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/likes/user`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${accessToken}`,
            }
        });
        const r = await response.json();
        setUserLikes(r.likes);
    };

    const refreshUser = async () => {
        const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/auth/user`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${firebaseUser.accessToken}`,
            }
        });
        const r = await response.json();
        if (r.user) {
            getUserLikes(firebaseUser.accessToken);
            getChats(firebaseUser.accessToken);
            setUser(r.user);
        }
    };

    const logout = async () => {
        await auth.signOut();
        setUser(null);
        setFirebaseUser(null);
        setLoading(true);
    };

    useEffect(() => {
        const unsubscribe = onAuthStateChanged(auth, async (firebaseUser) => {
            setLoading(true);

            if (!firebaseUser) {
                setUser(null);
                setFirebaseUser(null);
                setLoading(false);
                // Redirige a login si no hay usuario
                if (location.pathname !== '/login' && location.pathname !== '/register') {
                    navigate('/login');
                }
                return;
            }

            // Si ya hay un usuario autenticado y está intentando acceder a login o register, lo redirigimos
            if (firebaseUser && (location.pathname === "/login" || location.pathname === "/register")) {
                navigate("/"); // Redirige al home si ya está autenticado
                return;
            }
            try {
                const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/auth/user`, {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${firebaseUser.accessToken}`,
                    }
                });
                const r = await response.json();
                console.log(r)
                if (r.user) {
                    setUser(r.user);
                    setFirebaseUser(firebaseUser);
                    getUserLikes(firebaseUser.accessToken);
                    getChats(firebaseUser.accessToken);
                }
            } catch (error) {
                console.error(error);
                navigate("/login");
            } finally {
                setLoading(false);
            }
        });

        return () => unsubscribe();
    }, [location.pathname, navigate]);

    return (
        <AuthContext.Provider value={{ user, firebaseUser, userLikes, chats, loading, logout, refreshUser }}>
            {children}
        </AuthContext.Provider>
    );
};

// Hook personalizado para acceder al contexto
export const useAuth = () => {
    return useContext(AuthContext);
};
