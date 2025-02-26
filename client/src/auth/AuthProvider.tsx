import axios from "axios";
import { useLocation, useNavigate } from "react-router";
import { useLocalStorage } from "../hooks/useLocalStorage";
import { AuthContext } from "./AuthContext";


interface AuthProviderProps {
    children: React.ReactNode;
}


const AuthProvider = ({ children }: AuthProviderProps) => {
    const navigate = useNavigate();
    const location = useLocation();
    const [token, setToken] = useLocalStorage("access_token", null);

    const handleLogin = async (username: string, password: string) => {
        const form = new FormData();
        form.append('username', username);
        form.append('password', password);
        // TODO create client for axios
        const response = await axios.post(`${import.meta.env.API_URL as string}/login/access-token`, form)
        setToken(response.data.access_token);
        await navigate(location.state?.from?.pathname || '/game');
    };

    const handleLogout = async () => {
        setToken(null);
        await navigate('/login');
    };

    const value = {
        token,
        onLogin: handleLogin,
        onLogout: handleLogout,
    };

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};


export default AuthProvider;