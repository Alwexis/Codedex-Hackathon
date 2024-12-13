import { useEffect, useState } from "react"

export default function Loading() {
    const _MESSAGES_ = [
        "Hamsters are running as fast as they can...",
        "Our littles Fairies working hard to get your data...",
        "Our Hamsters are running to get your data...",
        "Our little Elves are working hard to get your data...",
    ]
    const [message, setMessage] = useState(_MESSAGES_[3]);

    useEffect(() => {
        const interval = setInterval(() => {
            setMessage(_MESSAGES_[Math.floor(Math.random() * _MESSAGES_.length)])
        }, 1500)

        return () => clearInterval(interval)
    }, [])
    
    return (
        <main className="h-screen w-screen flex flex-col items-center justify-center">
            <h1 className="font-vt323 font-bold text-5xl tracking-widest">WaveNet</h1>
            <h3 className="font-mono text-lg my-2 animate-pulse tracking-wider">Loading</h3>
            <p>{message}</p>
        </main>
    )
}