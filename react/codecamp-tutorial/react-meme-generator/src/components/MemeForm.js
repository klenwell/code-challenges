import React from 'react'


export default function MemeForm(props) {
  const [formData, setFormDate] = React.useState({
      topText: '',
      bottomText: ''
  })

  function handleClick() {
    props.setCaptionedMeme(prevMeme => {
      const newMeme = props.getRandomMeme()
      console.log(prevMeme)
      return {
        topText: formData.topText,
        bottomText: formData.bottomText,
        meme: newMeme
      }
    })
  }

  function changeHandler(e) {
    const {name, value} = e.target

    setFormDate(oldFormData => {
      return {
        ...oldFormData,
        [name]: value
      }
    })

    props.setCaptionedMeme(prevMeme => {
      return {
        ...prevMeme,
        [name]: value
      }
    })
  }

  return (
    <div className="meme-form">
      <input
        name="topText"
        type="text"
        value={formData.topText}
        onChange={changeHandler}
        placeholder="Shut up"
      />
      <input
        name="bottomText"
        type="text"
        value={formData.bottomText}
        onChange={changeHandler}
        placeholder="and take my money"
      />
      <button onClick={handleClick}>
        Get a new meme image
      </button>
    </div>
  )
}
