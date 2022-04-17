/*
Challenge: Starting from scratch, build and render the
HTML for our section project. Check the Google slide for
what you're trying to build.

We'll be adding styling to it later.

Hints:
* The React logo is a file in the project tree, so you can
  access it by using `src="./react-logo.png" in your image
  element
* You can also set the `width` attribute of the image element
  just like in HTML. In the slide, I have it set to 40px
 */

function Navbar() {
  return (
    <img className="nav-logo" src="./react-logo.svg" />
  )
}

function Header() {
  return (
    <h1 className="header">Fun Facts about React</h1>
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

const page = (
  <div>
    <Navbar />
    <Header />
    <FactList />
  </div>
)

const root = document.getElementById("root")

ReactDOM.render(page, root)
