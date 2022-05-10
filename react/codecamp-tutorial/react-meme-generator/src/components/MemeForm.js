import logoSrc from '../images/logo.png';

export default function MemeForm() {
  return (
    <form className="meme-form">
      <input type="text" placeholder="Shut up" />
      <input type="text" placeholder="and take my money" />
      <button>Get a new meme image</button>
    </form>
  )
}
