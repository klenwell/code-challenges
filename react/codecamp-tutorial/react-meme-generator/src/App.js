import './index.css'
import React from 'react'
import Header from './components/Header'
import MemeForm from './components/MemeForm'

export default function App() {
  const [things, setThings] = React.useState(['thing 1', 'thing 2'])
  const thingEls = things.map(thing => <p key={thing}>{thing}</p>)

  function addItem() {
    const idx = things.length + 1
    const nextThing = `Thing ${idx}`
    setThings(prevState => [...prevState, nextThing])
    console.log(things)
  }

  return (
    <div className="container">
      <Header />
      <main>
        <MemeForm />
        <button onClick={addItem}>Add Item</button>
        {thingEls}
      </main>
    </div>
  );
}
