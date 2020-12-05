function binaryAgent(str) {
  let binChars = str.split(' ')
  console.log(binChars)

  let chars = binChars.map(binChar => {
    let code = parseInt(binChar, 2)
    return String.fromCharCode(code)
  })

  console.log(chars)
  return chars.join('');
}

console.log(parseInt("01000001", 2))
console.log(String.fromCharCode(65))

binaryAgent("01000001 01110010 01100101 01101110 00100111 01110100 00100000 01100010 01101111 01101110 01100110 01101001 01110010 01100101 01110011 00100000 01100110 01110101 01101110 00100001 00111111");
