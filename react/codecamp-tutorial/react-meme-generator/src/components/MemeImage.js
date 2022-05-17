import React from 'react'


export default function MemeImage(props) {
  const captionedMeme = props.captionedMeme
  const src = captionedMeme.meme !== null ? captionedMeme.meme.url : ''
  const alt = `${captionedMeme.topText} ${captionedMeme.bottomText}`

  let content
  if ( src ) {
    content = (
      <div className="meme-image">
        <img src={src} alt={alt} />
        <h2 className="top">{captionedMeme.topText}</h2>
        <h2 className="bottom">{captionedMeme.bottomText}</h2>
      </div>
    )
  }
  else {
    content = <h4>Click button above</h4>
  }

  return content
}
