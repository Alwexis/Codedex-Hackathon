import React, { createContext, useState, useEffect, useContext } from 'react';
import { onAuthStateChanged } from 'firebase/auth';
import { auth } from "../firebase";
import { redirect } from 'react-router-dom';

// Crear un contexto
const AuthContext = createContext();

// Proveedor de contexto para envolver la aplicación
export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [firebaseUser, setFirebaseUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Establece el listener para el cambio de estado de autenticación
        const unsubscribe = onAuthStateChanged(auth, async (user) => {
            console.log(user)
            try {
                const _ = await fetch("http://localhost:8000/auth/user", {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${user.accessToken}`,
                    }
                });
                const r = await _.json();
                console.log(r.user);
                setUser(r.user);
                setFirebaseUser(user);
                // setLoading(false);
            } catch (error) {
                console.error(error);
                redirect("/login");
            }
        });

        // Limpieza del listener
        return () => unsubscribe();
    }, [auth]);

    return (
        <AuthContext.Provider value={{ user, firebaseUser, loading }}>
            {children}
        </AuthContext.Provider>
    );
};

// Hook personalizado para acceder al contexto
export const useAuth = () => {
    return useContext(AuthContext);
};
