const HTML_ENTITIES = {
  '&': '&amp;',
  '<': '&lt;',
  '>': '&gt;',
  '"': '&quot;',
  "'": '&apos;'
}

function convertHTML(str) {
  let charList = str.split('')

  let convertedHTML = charList.map(char => {
    let conversion = HTML_ENTITIES[char]
    return conversion === undefined ? char : conversion
  })

  console.log(convertedHTML)
  return convertedHTML.join('');
}

convertHTML("Dolce & Gabbana");
