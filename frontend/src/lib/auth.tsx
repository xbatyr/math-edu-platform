import { createContext, ReactNode, useContext, useEffect, useMemo, useState } from "react";

import { api, setUnauthorizedHandler, tokenStore } from "@/lib/api";
import type { AuthResponse, UserDto } from "@/types/api";

type AuthContextState = {
  user: UserDto | null;
  loading: boolean;
  login: (username: string, password: string) => Promise<void>;
  register: (username: string, email: string, password: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
};

const AuthContext = createContext<AuthContextState | undefined>(undefined);

async function fetchMe() {
  const userResponse = await api.get<UserDto>("/auth/me/");
  return userResponse.data;
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<UserDto | null>(null);
  const [loading, setLoading] = useState(true);

  const logout = () => {
    tokenStore.setAccess(null);
    tokenStore.setRefresh(null);
    setUser(null);
  };

  useEffect(() => {
    setUnauthorizedHandler(logout);
    const refresh = tokenStore.getRefresh();
    if (!refresh) {
      setLoading(false);
      return;
    }

    api
      .post("/auth/refresh/", { refresh })
      .then(async (res) => {
        tokenStore.setAccess(res.data.access);
        const restoredUser = await fetchMe();
        setUser(restoredUser);
      })
      .catch(() => logout())
      .finally(() => setLoading(false));
  }, []);

  const login = async (username: string, password: string) => {
    const { data } = await api.post<AuthResponse>("/auth/login/", { username, password });
    tokenStore.setAccess(data.access);
    tokenStore.setRefresh(data.refresh);
    setUser(data.user);
  };

  const register = async (username: string, email: string, password: string) => {
    const { data } = await api.post<AuthResponse>("/auth/register/", { username, email, password });
    tokenStore.setAccess(data.access);
    tokenStore.setRefresh(data.refresh);
    setUser(data.user);
  };

  const value = useMemo(
    () => ({ user, loading, login, register, logout, isAuthenticated: Boolean(user) }),
    [user, loading]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return context;
}
