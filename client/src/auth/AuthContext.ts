import { createContext } from "react";

export const AuthContext = createContext<{
    token: string | null;
    onLogin: (email: string, password: string) => Promise<void>;
    onLogout: () => Promise<void>;
}>({
    token: "",
    onLogin: async () => Promise.resolve(),
    onLogout: async () => Promise.resolve()
});

