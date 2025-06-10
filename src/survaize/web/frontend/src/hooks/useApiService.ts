import { useEffect, useRef } from "react";
import { SurvaizeApiService } from "../services/api";
import { logError } from "../services/logger";

export const useApiService = (): SurvaizeApiService => {
  const serviceRef = useRef<SurvaizeApiService>(new SurvaizeApiService());

  useEffect(() => {
    const checkApiConnection = async (): Promise<void> => {
      try {
        await fetch("/api/health");
      } catch (err) {
        logError("API connection failed", err);
      }
      serviceRef.current = new SurvaizeApiService();
    };

    void checkApiConnection();
  }, []);

  return serviceRef.current;
};
