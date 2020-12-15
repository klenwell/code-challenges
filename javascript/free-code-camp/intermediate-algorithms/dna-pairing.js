const BASE_PAIRS = {
  'A': 'T',
  'T': 'A',
  'C': 'G',
  'G': 'C'
}

function pairElement(str) {
  let pairedSequence = []
  let sequence = str.split('')

  pairedSequence = sequence.map(element => {
    let match = BASE_PAIRS[element]
    let pair = [element, match]
    return pair
  })
  return pairedSequence;
}

pairElement("GCG");
