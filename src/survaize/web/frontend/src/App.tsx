import { useState, useEffect } from "react";
import {
  QuestionnaireProvider,
  OpenQuestionnaire,
  SaveQuestionnaire,
} from "./components/QuestionnaireComponents";
import { QuestionnaireDisplay } from "./components/QuestionnaireDisplay";

const App: React.FC = () => {
  const [apiStatus, setApiStatus] = useState<string>("");
  const [isApiConnected, setIsApiConnected] = useState<boolean | null>(null);

  useEffect(() => {
    // Check API health
    fetch("/api/health")
      .then((response) => {
        if (!response.ok) throw new Error("API health check failed");
        setIsApiConnected(true);
        setApiStatus("");
      })
      .catch((error) => {
        console.error("Error fetching API:", error);
        setIsApiConnected(false);
        setApiStatus("⚠️ API connection failed");
      });
  }, []);

  return (
    <QuestionnaireProvider>
      <div className="app-container">
        <header className="app-header">
          <h1>Survaize</h1>
          <div
            className={`api-status ${isApiConnected === false ? "offline" : ""}`}
          >
            {isApiConnected === null ? (
              <span className="loading">Connecting to API...</span>
            ) : isApiConnected === false ? (
              <span className="offline">{apiStatus}</span>
            ) : null}
          </div>
        </header>

        <div className="toolbar">
          <OpenQuestionnaire />
          <SaveQuestionnaire />
        </div>

        <div className="main-content">
          <QuestionnaireDisplay />
        </div>
      </div>
    </QuestionnaireProvider>
  );
};

export default App;
