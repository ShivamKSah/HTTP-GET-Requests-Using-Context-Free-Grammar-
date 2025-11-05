import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Navigation } from './components/Navigation';
import { NotificationContainer } from './components/NotificationContainer';
import { LandingPage } from './pages/LandingPage';
import { ValidatorPage } from './pages/ValidatorPage';
import { AnalyticsPage } from './pages/AnalyticsPage';
import { LibraryPage } from './pages/LibraryPage';
import { ErrorsPage } from './pages/ErrorsPage';
import { GrammarPage } from './pages/GrammarPage';
import { AIAssistantPage } from './pages/AIAssistantPage';
import { APIProvider } from './contexts/APIContext';
import { NotificationProvider } from './contexts/NotificationContext';
import { ValidationProvider } from './contexts/ValidationContext';
import { FloatingAIButton } from './components/FloatingAIButton';
import { Footer } from './components/Footer';

function App() {
  return (
    <APIProvider>
      <NotificationProvider>
        <ValidationProvider>
        <Router>
          <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
            <Navigation />
            <NotificationContainer />
            <main className="min-h-screen">
              <Routes>
                <Route path="/" element={<LandingPage />} />
                <Route path="/validator" element={<ValidatorPage />} />
                <Route path="/analytics" element={<AnalyticsPage />} />
                <Route path="/library" element={<LibraryPage />} />
                <Route path="/errors" element={<ErrorsPage />} />
                <Route path="/grammar" element={<GrammarPage />} />
                <Route path="/assistant" element={<AIAssistantPage />} />
              </Routes>
            </main>
            <FloatingAIButton />
            <Footer />
          </div>
        </Router>
        </ValidationProvider>
      </NotificationProvider>
    </APIProvider>
  );
}

export default App;
