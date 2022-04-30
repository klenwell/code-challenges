import starImageSrc from '../images/star.png';

function Card(props) {
  const exp = props.experience
  const imgSrc = `/images/card-${exp.id}.png`
  let badgeText = null

  if (exp.openSpots === 0) {
    badgeText = 'SOLD OUT'
  }
  else if (exp.location === 'Online') {
    badgeText = 'ONLINE'
  }

  return (
    <div className="card">
      {badgeText && <div className="badge">{badgeText}</div>}
      <img className="header-image" src={imgSrc} alt="header-image" />
      <p className="stats">
        <img className="star" src={starImageSrc} alt="star" />
        <span className="rating">{exp.stats.rating}</span>
        <span className="count">({exp.stats.reviewCount})</span>
        &middot;
        <span className="location">{exp.location}</span>
      </p>
      <h4>{exp.title}</h4>
      <p className="price">From ${exp.price} / person</p>
    </div>
  )
}

export default Card
