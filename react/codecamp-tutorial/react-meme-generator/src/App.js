import './index.css'
import React from 'react'
import Header from './components/Header'
import MemeForm from './components/MemeForm'
import MemeImage from './components/MemeImage'
import memesData from './data/memes'

// Side Challenge: Sign Up Form
import SignUpForm from './components/SignUpForm'

export default function App() {
  const [captionedMeme, setCaptionedMeme] = React.useState({
    topText: "",
    bottomText: "",
    meme: getRandomMeme()
  })

  function getRandomMeme() {
    const memes = memesData['data']['memes']
    const randomIndex = randomInteger(0, memes.length)
    return memes[randomIndex]
  }

  function randomInteger(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
  }

  return (
    <div className="container">
      <Header />
      <main>
        <MemeForm
          captionedMeme={captionedMeme}
          setCaptionedMeme={setCaptionedMeme}
          getRandomMeme={getRandomMeme}
        />
        <MemeImage captionedMeme={captionedMeme} />
      </main>
    </div>
  );
}
