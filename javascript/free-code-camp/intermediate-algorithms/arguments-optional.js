function addTogether() {
  let args = [...arguments]
  console.log('args', args)

  if ( !Number.isInteger(args[0]) ) {
    return undefined
  }

  if (args.length === 1) {
    var func = function(num) {
      return addTogether(num, args[0])
    }
    return func
  }
  else {
    return Number.isInteger(args[1]) ? args[0] + args[1] : undefined
  }
}

addTogether(5)(7)
