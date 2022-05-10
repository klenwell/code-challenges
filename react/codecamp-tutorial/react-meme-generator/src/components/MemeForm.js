import memesData from '../data/memes'


export default function MemeForm() {
  function handleClick(e) {
    const memes = memesData['data']['memes']
    const randomNum = randomInteger(0, memes.length)
    const randomMeme = memes[randomNum]
    console.log(randomMeme)
  }

  function handleMouseOver(e) {
    console.log("Mouse over!")
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
    </div>
  )
}
