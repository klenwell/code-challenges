import logo from '../logo.svg';

function Navbar() {
  return (
    <nav>
      <img className="nav-logo" src={logo} alt="logo" />
      <h2>React Facts</h2>
      <h3>React Course - Project 1</h3>
    </nav>
  )
}

export default Navbar
