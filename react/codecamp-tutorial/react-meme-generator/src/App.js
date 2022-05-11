import './index.css'
import React from 'react'
import Header from './components/Header'
import MemeForm from './components/MemeForm'

export default function App() {
  return (
    <div className="container">
      <Header />
      <main>
        <MemeForm />
      </main>
    </div>
  );
}
