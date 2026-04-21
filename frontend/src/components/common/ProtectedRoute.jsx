import { Navigate } from "react-router-dom";
import authStore from "../../store/authStore";

export default function ProtectedRoute({ children }) {
  if (!authStore.isAuthenticated()) {
    return <Navigate to="/convert" replace />;
  }

  return children;
}