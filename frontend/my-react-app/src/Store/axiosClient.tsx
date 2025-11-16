// axiosClient.ts
import axios from "axios";
import { useAuthStore } from "./useAuthStore";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
  withCredentials: true,     // include refresh cookie
});

// ⬇ Auto-attach access token
api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().accessToken;
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// ⬇ Auto-refresh on 401
api.interceptors.response.use(
  (res) => res,
  async (error) => {
    const originalRequest = error.config;

    // Token expired?
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshRes = await axios.post(
          "http://127.0.0.1:8000/refresh",
          {},
          { withCredentials: true }
        );

        const newAccessToken = refreshRes.data.access_token;

        useAuthStore.getState().setAccessToken(newAccessToken);

        // Retry original request
        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
        return api(originalRequest);

      } catch (refreshError) {
        useAuthStore.getState().logout();
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default api;
