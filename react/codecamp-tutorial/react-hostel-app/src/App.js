import './App.css'
import Navbar from './components/Navbar'
import Hero from './components/Hero'
import Card from './components/Card'
import experiencesData from './data/experiences'

function App() {
  const cardElements = experiencesData.map(experience => {
    return <Card
      key={experience.id}
      experience={experience}
    />
  })
  return (
    <div className="container">
      <Navbar />
      <Hero />
      <section className="cards">
        {cardElements}
      </section>
    </div>
  );
}

export default App;
