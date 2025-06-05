import React, { useState } from 'react';
import PhaserGame from './components/PhaserGame';
import { Logo } from './components/Logo';
import { WelcomeScreen } from './components/WelcomeScreen';
import './App.css';

function App() {
  const [showWelcome, setShowWelcome] = useState(true);

  return (
    <div className="App">
      <header className="border-b border-gray-700 px-6" style={{ backgroundColor: 'rgb(235, 225, 204)' }}>
        <Logo />
      </header>
      {showWelcome ? (
        <WelcomeScreen onNext={() => setShowWelcome(false)} />
      ) : (
        <div className="flex-1 flex items-center justify-center p-6">
          <PhaserGame />
        </div>
      )}
    </div>
  );
}

export default App;
