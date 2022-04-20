import hero_image_src from '../images/hero.png';

function Hero() {
  return (
    <section className="hero">
      <div className="photo-grid"><img src={hero_image_src} alt="photo-grid" /></div>
      <h1>Online Experiences</h1>
      <p>Join unique interactive activies led by one-of-a-kind hosts—all without
         leaving home.</p>
    </section>
  )
}

export default Hero
