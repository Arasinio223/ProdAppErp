
import React, { useState, useEffect } from 'react';

const Main = () => {
    const [user, setUser] = useState(null);
    const [status, setStatus] = useState('');
    const [zlecenia, setZlecenia] = useState([]);
    const [statusy, setStatusy] = useState([]);
    const [showZleceniaModal, setShowZleceniaModal] = useState(false);

    useEffect(() => {
        const fetchInitialData = async () => {
            const userResponse = await fetch('/api/user/');
            const userData = await userResponse.json();
            setUser(userData);

            const statusResponse = await fetch(`/api/status/${userData.id}/`);
            const statusData = await statusResponse.json();
            setStatus(statusData.status);

            const zleceniaResponse = await fetch('/api/zlecenia/');
            const zleceniaData = await zleceniaResponse.json();
            setZlecenia(zleceniaData);

            const statusyResponse = await fetch('/api/statusy/');
            const statusyData = await statusyResponse.json();
            setStatusy(statusyData);
        };
        fetchInitialData();
    }, []);

    const handleStatusChange = (newStatus) => {
        if (newStatus === 'Praca') {
            setShowZleceniaModal(true);
        } else {
            updateStatus(newStatus);
        }
    };

    const handleZlecenieSelect = (zlecenie) => {
        updateStatus('Praca', zlecenie.id);
        setShowZleceniaModal(false);
    };

    const updateStatus = async (newStatus, zlecenieId = null) => {
        await fetch('/api/change-status/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                user_id: user.id,
                status: newStatus,
                zlecenie_id: zlecenieId,
            }),
        });
        setStatus(newStatus);
    };

    if (!user) {
        return <div>Loading...</div>;
    }

    return (
        <div>
            {user.is_staff && <a href="/admin">Manager Panel</a>}
            <h1>Witaj, {user.first_name} {user.last_name}</h1>
            <h2>Aktualny status: {status}</h2>

            <div>
                {statusy.map((s) => (
                    <button key={s.id} onClick={() => handleStatusChange(s.nazwa)}>
                        {s.nazwa}
                    </button>
                ))}
            </div>

            {showZleceniaModal && (
                <div className="modal">
                    <div>
                        <h2>Wybierz zlecenie</h2>
                        <ul>
                            {zlecenia.map((zlecenie) => (
                                <li key={zlecenie.id} onClick={() => handleZlecenieSelect(zlecenie)}>
                                    {zlecenie.nazwa}
                                </li>
                            ))}
                        </ul>
                        <button onClick={() => setShowZleceniaModal(false)}>Anuluj</button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default Main;
