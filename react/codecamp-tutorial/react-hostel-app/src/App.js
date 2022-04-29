import './App.css'
import Navbar from './components/Navbar'
import Hero from './components/Hero'
import Card from './components/Card'
import experiencesData from './data/experiences'

function App() {
  const cardElements = experiencesData.map(experience => {
    return <Card
      id={experience.id}
      title={experience.title}
      rating={experience.stats.rating}
      count={experience.stats.reviewCount}
      price={experience.price}
      location={experience.location}
      openSpots={experience.openSpots}
    />
  })
  return (
    <div className="container">
      <Navbar />
      <section className="cards">
        {cardElements}
      </section>
      <Hero />
    </div>
  );
}

export default App;
