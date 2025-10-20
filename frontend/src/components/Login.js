
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Login = () => {
    const [login, setLogin] = useState('');
    const [pin, setPin] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleLogin = async () => {
        if (pin.length !== 6) {
            setError('PIN must be 6 digits');
            return;
        }
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
            <h1 data-testid="login-heading">Login</h1>
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
                placeholder="PIN (6 digits)"
                maxLength="6"
            />
            <button onClick={handleLogin}>Login</button>
            {error && <p>{error}</p>}
            <p>Or use RFID card</p>
        </div>
    );
};

export default Login;
