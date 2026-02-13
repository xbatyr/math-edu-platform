import axios, { AxiosError, InternalAxiosRequestConfig } from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8001/api/v1";

let accessToken: string | null = null;
let onUnauthorized: (() => void) | null = null;

export const tokenStore = {
  getAccess: () => accessToken,
  setAccess: (token: string | null) => {
    accessToken = token;
  },
  getRefresh: () => localStorage.getItem("refresh_token"),
  setRefresh: (token: string | null) => {
    if (!token) {
      localStorage.removeItem("refresh_token");
      return;
    }
    localStorage.setItem("refresh_token", token);
  },
};

export const setUnauthorizedHandler = (handler: (() => void) | null) => {
  onUnauthorized = handler;
};

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: { "Content-Type": "application/json" },
});

api.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  const token = tokenStore.getAccess();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as InternalAxiosRequestConfig & { _retry?: boolean };

    if (error.response?.status !== 401 || originalRequest?._retry) {
      return Promise.reject(error);
    }

    const refresh = tokenStore.getRefresh();
    if (!refresh) {
      if (onUnauthorized) onUnauthorized();
      return Promise.reject(error);
    }

    originalRequest._retry = true;

    try {
      const refreshResponse = await axios.post(`${API_BASE_URL}/auth/refresh/`, { refresh });
      const nextAccess = refreshResponse.data.access as string;
      tokenStore.setAccess(nextAccess);
      originalRequest.headers.Authorization = `Bearer ${nextAccess}`;
      return api(originalRequest);
    } catch (refreshError) {
      tokenStore.setAccess(null);
      tokenStore.setRefresh(null);
      if (onUnauthorized) onUnauthorized();
      return Promise.reject(refreshError);
    }
  }
);
