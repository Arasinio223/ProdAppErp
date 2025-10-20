
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Login = () => {
    const [login, setLogin] = useState('');
    const [pin, setPin] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleLogin = async () => {
        const response = await fetch('/api/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ login, pin }),
        });
        if (response.ok) {
            navigate('/main');
        } else {
            setError('Invalid credentials');
        }
    };

    return (
        <div>
            <h1>Login</h1>
            <input
                type="text"
                value={login}
                onChange={(e) => setLogin(e.target.value)}
                placeholder="Login (4 letters)"
            />
            <input
                type="password"
                value={pin}
                onChange={(e) => setPin(e.target.value)}
                placeholder="PIN (4 digits)"
            />
            <button onClick={handleLogin}>Login</button>
            {error && <p>{error}</p>}
            <p>Or use RFID card</p>
        </div>
    );
};

export default Login;
