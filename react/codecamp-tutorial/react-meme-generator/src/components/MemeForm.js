import memesData from '../data/memes'
import React from 'react'


export default function MemeForm() {
  const [meme, setMeme] = React.useState(getRandomMeme())

  function getRandomMeme() {
    const memes = memesData['data']['memes']
    const randomIndex = randomInteger(0, memes.length)
    return memes[randomIndex]
  }

  function handleClick() {
    setMeme(prevMeme => {
      console.log(prevMeme)
      return getRandomMeme()
    })
  }

  function handleMouseOver(e) {
    console.log("Mouse over!", e)
  }

  function randomInteger(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
  }

  return (
    <div className="meme-form">
      <input type="text" placeholder="Shut up" />
      <input type="text" placeholder="and take my money" />
      <button
        onClick={handleClick}
        onMouseOver={handleMouseOver}>
        Get a new meme image
      </button>
      <img src={meme.url} alt={meme.name} />
    </div>
  )
}
