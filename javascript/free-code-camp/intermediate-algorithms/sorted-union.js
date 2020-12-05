function uniteUnique(arr) {
  let args = [...arguments]
  let sortedUnion = []
  console.log(args)
  
  args.forEach(subArr => {
    subArr.forEach(member => {
      if ( ! sortedUnion.includes(member) ) {
        sortedUnion.push(member)
      } 
    })
  })

  return sortedUnion;
}

uniteUnique([1, 3, 2], [5, 2, 1, 4], [2, 1]);
