import { Navigate } from "react-router-dom";
import { useAuthStore } from "../Store/useAuthStore";

export default function ProtectedRoute({ children }: { children: JSX.Element }) {
  const accessToken = useAuthStore(state => state.accessToken);

  if (!accessToken) {
    return <Navigate to="/login" replace />;
  }

  return children;
}
