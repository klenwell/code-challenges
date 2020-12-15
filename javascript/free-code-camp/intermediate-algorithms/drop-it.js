function dropElements(arr, func) {
  let undroppedElements = []
  let foundTrue = false

  arr.forEach(n => {
    if ( ! foundTrue ) {
      foundTrue = func(n)
    }
     
    if ( foundTrue ) {
      undroppedElements.push(n)
    }
  })
  
  console.log(undroppedElements)
  return undroppedElements;
}

dropElements([1, 2, 3], function(n) {return n < 3; });
