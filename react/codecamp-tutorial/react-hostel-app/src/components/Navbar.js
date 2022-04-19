import logo from '../images/logo.png';

function Navbar() {
  return (
    <nav>
      <img className="nav-logo" src={logo} alt="logo" />
      <h4>AirHostel</h4>
    </nav>
  )
}

export default Navbar
