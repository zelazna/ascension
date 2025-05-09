import { useState, useEffect } from "react";

function getStorageValue<T>(key: string, defaultValue: T): T {
    const saved = localStorage.getItem(key);
    const initial: T = saved ? JSON.parse(saved) as T : defaultValue;
    return initial || defaultValue;
}

export const useLocalStorage = <T,>(key: string, defaultValue: T): [T, (value: T) => void] => {
    const [value, setValue] = useState(() => {
        return getStorageValue(key, defaultValue);
    });

    useEffect(() => {
        localStorage.setItem(key, JSON.stringify(value));
    }, [key, value]);

    return [value, setValue];
};