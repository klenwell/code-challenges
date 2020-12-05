const ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

function fearNotLetter(str) {
  let missingLetter = undefined
  let incompleteRange = str.split('')
  let startRange = incompleteRange[0]
  let inRange = false
  
  ALPHABET.split('').forEach(letter => {
    if ( letter === startRange ) {
      inRange = true
    }

    if ( inRange ) {
      if ( ! incompleteRange.includes(letter) ) {
        missingLetter = letter
        inRange = false
      }
    }

    console.log(letter, startRange, inRange)
    return inRange
  })

  console.log(missingLetter)
  return missingLetter;
}

fearNotLetter("stvwx");
