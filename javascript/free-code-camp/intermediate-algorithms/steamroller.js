function steamrollArray(arr) {
  console.log('in', arr)
  let flatArr = []
  arr.forEach(v => {
    if ( Array.isArray(v) ) {
      // flatception!
      let flatterArr = steamrollArray(v)
      flatArr = flatArr.concat(flatterArr)
    }
    else {
      flatArr.push(v)
    }
    console.log('->', flatArr)
  })
  console.log('out', flatArr)
  return flatArr;
}

steamrollArray([1, [2], [3, [[4]]]]);
