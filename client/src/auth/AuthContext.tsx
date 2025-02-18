import { createContext } from "react";

export const AuthContext = createContext<{
    token: string;
    onLogin: (email: string, password: string) => Promise<void>;
    onLogout: () => void;
}>({
    token: "",
    onLogin: async () => {},
    onLogout: () => {}
});
