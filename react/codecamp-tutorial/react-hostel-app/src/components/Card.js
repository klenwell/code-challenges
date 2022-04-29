import starImageSrc from '../images/star.png';

function Card(props) {
  const imgSrc = `/images/card-${props.id}.png`
  let badgeText = null

  if (props.openSpots === 0) {
    badgeText = 'SOLD OUT'
  }
  else if ( props.location === 'Online' ) {
    badgeText = 'ONLINE'
  }

  return (
    <div className="card">
      {badgeText && <div className="badge">{badgeText}</div>}
      <img className="header-image" src={imgSrc} alt="header-image" />
      <p className="stats">
        <img className="star" src={starImageSrc} alt="star" />
        <span className="rating">{props.rating}</span>
        <span className="count">({props.count})</span>
        &middot;
        <span className="location">{props.location}</span>
      </p>
      <h4>{props.title}</h4>
      <p className="price">From ${props.price} / person</p>
    </div>
  )
}

export default Card
