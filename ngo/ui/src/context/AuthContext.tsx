"use client";

import { createContext, useContext, ReactNode } from "react";

/** Local demo auth until Keycloak / AWE staff realm is wired. */
interface AuthUser {
  name: string;
  preferred_username: string;
  email: string;
}

interface AuthContextType {
  user: AuthUser;
  logout: () => void;
}

const DEMO_USER: AuthUser = {
  name: "OPM Staff",
  preferred_username: "opm.staff",
  email: "staff@opm.go.ug",
};

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const logout = () => {
    window.location.href = "/";
  };
  return (
    <AuthContext.Provider value={{ user: DEMO_USER, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
