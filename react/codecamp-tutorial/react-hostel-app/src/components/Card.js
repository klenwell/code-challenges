import star from '../images/star.png';

function Card({title, imgNum, rating, count, country, cost}) {
  const imgSrc = `/images/card-${imgNum}.png`;

  return (
    <div className="card">
      <img className="header-image" src={imgSrc} alt="header-image" />
      <p className="stats">
        <img className="star" src={star} alt="star" />
        <span className="rating">{rating}</span>
        <span className="count">({count})</span>
        &middot;
        <span className="country">{country}</span>
      </p>
      <h4>{title}</h4>
      <p className="cost">From ${cost} / person</p>
    </div>
  )
}

export default Card
