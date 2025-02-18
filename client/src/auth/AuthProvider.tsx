import { useState } from "react";
import { AuthContext } from "./AuthContext";
import { useLocation, useNavigate } from "react-router";
// import axios from "axios";


interface AuthProviderProps {
    children: React.ReactNode;
}

const fakeAuth = (d: any): Promise<string> =>
    new Promise((resolve) => {
        setTimeout(() => { resolve({ data: { access_token: "2342f2f1d131rf12" } }); }, 250);
    });

const AuthProvider = ({ children }: AuthProviderProps) => {
    const navigate = useNavigate();
    const location = useLocation();
    const [token, setToken] = useState("");

    const handleLogin = async (email: string, password: string) => {
        const requestBody = { email, password }
        // const response = await axios.post('TODO', requestBody)
        const response = await fakeAuth(requestBody)
        setToken(response.data.access_token);
        // localStorage.setItem('access_token', response.data.access_token)
        await navigate(location.state?.from?.pathname || '/game');
    };

    const handleLogout = () => {
        setToken("");
    };

    const value = {
        token,
        onLogin: handleLogin,
        onLogout: handleLogout,
    };

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};


export default AuthProvider;