import logo from '../logo.svg';

function Navbar() {
  return (
    <nav>
      <img className="nav-logo" src={logo} alt="logo" />
      <ul className="nav-items">
        <li>Item 1</li>
      </ul>
    </nav>
  )
}

export default Navbar
