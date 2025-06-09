import React, { useState, useRef, useEffect } from 'react';
import { Questionnaire } from '../models/questionnaire';
import { SurvaizeApiService } from '../services/api';

interface QuestionnaireContextType {
  questionnaire: Questionnaire | null;
  setQuestionnaire: (questionnaire: Questionnaire | null) => void;
  isSaving: boolean;
  isLoading: boolean;
  setIsLoading: (loading: boolean) => void;
  loadProgress: number;
  setLoadProgress: (progress: number) => void;
  loadMessage: string;
  setLoadMessage: (message: string) => void;
  errorMessage: string | null;
  setErrorMessage: (message: string | null) => void;
}

// Create context with default values
export const QuestionnaireContext = React.createContext<QuestionnaireContextType>({
  questionnaire: null,
  setQuestionnaire: () => {},
  isSaving: false,
  isLoading: false,
  setIsLoading: () => {},
  loadProgress: 0,
  setLoadProgress: () => {},
  loadMessage: '',
  setLoadMessage: () => {},
  errorMessage: null,
  setErrorMessage: () => {}
});

interface QuestionnaireProviderProps {
  children: React.ReactNode;
}

export const QuestionnaireProvider: React.FC<QuestionnaireProviderProps> = ({ children }) => {
  const [questionnaire, setQuestionnaire] = useState<Questionnaire | null>(null);
  const [isSaving, setIsSaving] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [loadProgress, setLoadProgress] = useState(0);
  const [loadMessage, setLoadMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const value = {
    questionnaire,
    setQuestionnaire,
    isSaving,
    isLoading,
    setIsLoading,
    loadProgress,
    setLoadProgress,
    loadMessage,
    setLoadMessage,
    errorMessage,
    setErrorMessage
  };

  return (
    <QuestionnaireContext.Provider value={value}>
      {children}
    </QuestionnaireContext.Provider>
  );
};

// Custom hook to use the questionnaire context
export const useQuestionnaire = () => {
  const context = React.useContext(QuestionnaireContext);
  if (context === undefined) {
    throw new Error('useQuestionnaire must be used within a QuestionnaireProvider');
  }
  return context;
};

// Component for opening a questionnaire
export const OpenQuestionnaire: React.FC = () => {
  const {
    setQuestionnaire,
    isLoading,
    setIsLoading,
    setLoadProgress,
    setLoadMessage
  } = useQuestionnaire();
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  
  // Check if the API is available or if we're working in offline mode
  const [isOfflineMode, setIsOfflineMode] = useState(false);
  const apiService = useRef(new SurvaizeApiService(isOfflineMode));

  // Check API connectivity on mount
  useEffect(() => {
    const checkApiConnection = async () => {
      try {
        const response = await fetch('/api/health');
        const isOffline = !response.ok;
        setIsOfflineMode(isOffline);
        apiService.current = new SurvaizeApiService(isOffline);
      } catch (error) {
        console.warn('API connection failed, using mock data');
        setIsOfflineMode(true);
        apiService.current = new SurvaizeApiService(true);
      }
    };
    
    checkApiConnection();
  }, []);

  const [processingPdf, setProcessingPdf] = useState(false);
  
  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files || files.length === 0) {
      return;
    }

    const file = files[0];
    const fileExt = file.name.split('.').pop()?.toLowerCase();

    if (fileExt !== 'pdf' && fileExt !== 'json') {
      setError('Unsupported file format. Please select a PDF or JSON file.');
      return;
    }

    setIsLoading(true);
    setError(null);
    
    setProcessingPdf(fileExt === 'pdf');

    try {
      const loadedQuestionnaire = await apiService.current.readQuestionnaire(file, (progress, message) => {
        console.log('Progress update:', progress, message);
        setLoadProgress(progress);
        setLoadMessage(message);
      });
      console.log('Questionnaire loaded successfully:', loadedQuestionnaire);
      setLoadProgress(100);
      setQuestionnaire(loadedQuestionnaire);
    } catch (err) {
      console.error('Error loading questionnaire:', err);
      setError(`Failed to load questionnaire: ${err instanceof Error ? err.message : 'Unknown error'}`);
    } finally {
      setProcessingPdf(false);
      setLoadProgress(0);
      setLoadMessage('');
      setIsLoading(false);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };

  const handleOpenClick = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  return (
    <div>
      <input
        type="file"
        ref={fileInputRef}
        style={{ display: 'none' }}
        onChange={handleFileChange}
        accept=".pdf,.json"
      />
      <button
        onClick={handleOpenClick}
        disabled={isLoading}
        className="action-button"
      >
        {isLoading ? (processingPdf ? 'Processing PDF...' : 'Opening...') : 'Open Questionnaire'}
      </button>
      {error && <div className="error-message">{error}</div>}
    </div>
  );
};

// Component for saving a questionnaire
export const SaveQuestionnaire: React.FC = () => {
  const { questionnaire } = useQuestionnaire();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  // Check if the API is available or if we're working in offline mode
  const [isOfflineMode, setIsOfflineMode] = useState(false);
  const apiService = useRef(new SurvaizeApiService(isOfflineMode));

  // Check API connectivity on mount
  useEffect(() => {
    const checkApiConnection = async () => {
      try {
        const response = await fetch('/api/health');
        const isOffline = !response.ok;
        setIsOfflineMode(isOffline);
        apiService.current = new SurvaizeApiService(isOffline);
      } catch (error) {
        console.warn('API connection failed, using mock data');
        setIsOfflineMode(true);
        apiService.current = new SurvaizeApiService(true);
      }
    };
    
    checkApiConnection();
  }, []);

  const handleSave = async (format: 'json' | 'cspro') => {
    if (!questionnaire) {
      setError('No questionnaire to save. Please open a questionnaire first.');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      // Show a warning if in offline mode and trying to save as CSPro
      if (isOfflineMode && format === 'cspro') {
        const confirmOffline = window.confirm(
          'You are in offline mode. CSPro conversion requires a server connection. Continue with a simplified version?'
        );
        if (!confirmOffline) {
          setIsLoading(false);
          return;
        }
      }

      const blob = await apiService.current.saveQuestionnaire(questionnaire, format);
      
      // Create a download link and trigger download
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      const fileExtension = format === 'json' ? 'json' : (isOfflineMode ? 'txt' : 'zip');
      a.download = `${questionnaire.title.replace(/\s+/g, '_')}.${fileExtension}`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (err) {
      setError(`Failed to save questionnaire: ${err instanceof Error ? err.message : 'Unknown error'}`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="save-actions">
      <button 
        onClick={() => handleSave('json')} 
        disabled={isLoading || !questionnaire}
        className="action-button"
      >
        {isLoading ? 'Saving...' : 'Save as JSON'}
      </button>
      <button 
        onClick={() => handleSave('cspro')} 
        disabled={isLoading || !questionnaire}
        className="action-button"
      >
        {isLoading ? 'Saving...' : 'Save as CSPro'}
      </button>
      {error && <div className="error-message">{error}</div>}
    </div>
  );
};
