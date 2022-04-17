/**
Challenge:

Part 1: Create a page of your own using a custom Page component

It should return an ordered list with the reasons why you're
excited to be learning React :)

Render your list to the page

 */
function Navbar() {
  return (
    <nav>
      <img className="nav-logo" src="./react-logo.svg" />
    </nav>
  )
}

function Header() {
  return (
    <h1 className="header">Fun Facts about React (Component Version)</h1>
  )
}

function FactList() {
  return (
    <ul>
      <li>Was first released in 2013</li>
      <li>Was originally created by Jordan Walke</li>
      <li>Has well over 100k stars on Github</li>
      <li>Is maintained by Facebook</li>
      <li>Powers thousands of enterprise apps, including mobile apps</li>
    </ul>
  )
}

function Footer() {
  return (
    <footer>
      <small>Some rights reserved, ©2022</small>
    </footer>
  )
}

function Page() {
  return (
    <div>
      <Navbar />
      <Header />
      <FactList />
      <Footer />
    </div>
  )
}

const root = document.getElementById("root")

ReactDOM.render(<Page />, root)
