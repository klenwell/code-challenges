import logoSrc from '../images/logo.png';

export default function Header() {
  return (
    <header>
      <img className="logo" src={logoSrc} alt="logo" />
      <h2>Meme Generator</h2>
      <h4>React Course - Project 3</h4>
    </header>
  )
}
