// // // useAuthStore.ts
// import { create } from "zustand";

// // interface AuthState {
// //   accessToken: string | null;
// //   setAccessToken: (token: string | null) => void;
// //   logout: () => void;
// // }

// // export const useAuthStore = create<AuthState>((set) => ({
// //   accessToken: null,

// //   setAccessToken: (token) => set({ accessToken: token }),

// //   logout: () => set({ accessToken: null }),
// // }));


// export const useAuthStore = create((set) => ({
//   accessToken: localStorage.getItem("access_token") || null,
//   setAccessToken: (token) => {
//     localStorage.setItem("access_token", token);
//     set({ accessToken: token });
//   },
//   // clearToken: () => {
//   //   localStorage.removeItem("access_token");
//   //   set({ accessToken: null });
//   // }
//   logout: () => {
//   localStorage.removeItem("access_token"); // optional if you used LS
//   set({ accessToken: null });
// }

// }));

import { create } from "zustand";

export const useAuthStore = create((set, get) => ({
  accessToken: localStorage.getItem("access_token") || null,
  tokenExpiry: Number(localStorage.getItem("token_expiry")) || null,

  // Save token + expiry
  setAccessToken: (token) => {
    const expiresAt = Date.now() + 5 * 60 * 1000; // 5 minutes

    localStorage.setItem("access_token", token);
    localStorage.setItem("token_expiry", expiresAt.toString());

    set({ accessToken: token, tokenExpiry: expiresAt });

    // Start the auto-expire timer
    get().startExpiryTimer();
  },

  logout: () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("token_expiry");
    set({ accessToken: null, tokenExpiry: null });
  },

  // ⏳ auto-expire token
  startExpiryTimer: () => {
    const { tokenExpiry, logout } = get();
    if (!tokenExpiry) return;

    const delay = tokenExpiry - Date.now();

    if (delay <= 0) {
      logout();
      return;
    }

    setTimeout(() => {
      logout();
      console.log("Access token expired after 5 minutes");
    }, delay);
  },
}));

