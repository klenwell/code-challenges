import './index.css'
import React from 'react'
import Header from './components/Header'
import MemeForm from './components/MemeForm'

export default function App() {
  const [buttonText, setButtonText] = React.useState(['Click Me'])

  function handleHover() {
    setButtonText('Hovered...')
  }

  function handleClick() {
    setButtonText('Clicked!')
  }

  return (
    <div className="container">
      <Header />
      <main>
        <MemeForm />
        <button onMouseOver={handleHover} onClick={handleClick}>{buttonText}</button>
      </main>
    </div>
  );
}
