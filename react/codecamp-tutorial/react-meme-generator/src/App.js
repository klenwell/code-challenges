import './index.css'
import React from 'react'
import Header from './components/Header'
import MemeForm from './components/MemeForm'
import MemeImage from './components/MemeImage'
//import memesData from './data/memes'


const API_URL = 'https://api.imgflip.com/get_memes'


export default function App() {
  const [captionedMeme, setCaptionedMeme] = React.useState({
    topText: "",
    bottomText: "",
    meme: null
  })

  const [memesData, setMemesData] = React.useState({})

  function getRandomMeme() {
    const memes = memesData
    const randomIndex = randomInteger(0, memes.length)
    return memes[randomIndex]
  }

  function randomInteger(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
  }

  React.useEffect(() => {
    fetch(API_URL)
      .then(response => response.json())
      .then(data => setMemesData(data.data.memes))
  }, [])

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
