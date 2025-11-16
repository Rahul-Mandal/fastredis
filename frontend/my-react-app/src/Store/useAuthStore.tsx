// // useAuthStore.ts
import { create } from "zustand";

// interface AuthState {
//   accessToken: string | null;
//   setAccessToken: (token: string | null) => void;
//   logout: () => void;
// }

// export const useAuthStore = create<AuthState>((set) => ({
//   accessToken: null,

//   setAccessToken: (token) => set({ accessToken: token }),

//   logout: () => set({ accessToken: null }),
// }));


export const useAuthStore = create((set) => ({
  accessToken: localStorage.getItem("access_token") || null,
  setAccessToken: (token) => {
    localStorage.setItem("access_token", token);
    set({ accessToken: token });
  },
  clearToken: () => {
    localStorage.removeItem("access_token");
    set({ accessToken: null });
  }
}));
