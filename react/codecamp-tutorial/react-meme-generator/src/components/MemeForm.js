import React from 'react'


export default function MemeForm(props) {
  function handleClick() {
    props.setCaptionedMeme(prevMeme => {
      const newMeme = props.getRandomMeme()
      console.log(prevMeme)
      return {
        // TODO: Replace with input values.
        topText: newMeme.name,
        bottomText: "TODO",
        meme: newMeme
      }
    })
  }

  function handleMouseOver(e) {
    console.log("Mouse over!", e)
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
