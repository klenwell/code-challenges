import React from 'react'


export default function MemeImage(props) {
  const captionedMeme = props.captionedMeme
  const src = captionedMeme.meme.url
  const alt = `${captionedMeme.topText} ${captionedMeme.bottomText}`

  return (
    <div className="meme-image">
      <h4>{captionedMeme.topText}</h4>
      <h4>{captionedMeme.bottomText}</h4>
      <img src={src} alt={alt} />
    </div>
  )
}
