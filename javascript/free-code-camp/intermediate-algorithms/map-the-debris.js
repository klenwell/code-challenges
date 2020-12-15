function orbitalPeriod(arr) {
  var GM = 398600.4418;
  var earthRadius = 6367.4447;

  let debrisMap = arr.map(orbiter => {
    let T = earthOrbitalPeriod(orbiter.avgAlt)

    return {
      name: orbiter.name,
      orbitalPeriod: T
    };
  })

  console.log(debrisMap)
  return debrisMap
}

function earthOrbitalPeriod(avgAlt) {
  const GM = 398600.4418;
  const earthRadius = 6367.4447;

  // https://en.wikipedia.org/wiki/Orbital_period#Small_body_orbiting_a_central_body
  let a = earthRadius + avgAlt
  let T = 2 * Math.PI * Math.sqrt(Math.pow(a, 3) / GM)
  return Math.round(T)
}

console.log(Math.PI, Math.pow(2,2), Math.sqrt(4))
orbitalPeriod([{name : "sputnik", avgAlt : 35873.5553}]);
