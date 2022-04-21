import './App.css'
import Navbar from './components/Navbar'
import Hero from './components/Hero'
import Card from './components/Card'
import experiencesData from './data/experiences'

function App() {
  const cardElements = experiencesData.map(experience => {
    return <Card
      key={experience.id}
      title={experience.title}
      imgNum={experience.imgNum}
      rating={experience.rating}
      count={experience.count}
      cost={experience.cost}
      country={experience.country}
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
