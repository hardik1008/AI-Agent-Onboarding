"use client";

import { useEffect, useState } from "react";
import { api } from "./api";
import type { AuthConfig } from "./types";

export function useAuthConfig(): AuthConfig | null {
  const [config, setConfig] = useState<AuthConfig | null>(null);
  useEffect(() => {
    api<AuthConfig>("/auth/config").then(setConfig, () => setConfig(null));
  }, []);
  return config;
}
