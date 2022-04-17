import logo from './logo.svg';

function Navbar() {
  return (
    <nav>
      <img className="nav-logo" src={logo} alt="logo" />
      <ul className="nav-items">
        <li>Pricing</li>
        <li>About</li>
        <li>Contact</li>
      </ul>
    </nav>
  )
}

function Header() {
  return (
    <header>
      <Navbar />
      <h1 className="header">Fun Facts about React (Component Version)</h1>
    </header>
  )
}

export default Header
