function sumFibs(num) {
  let nextNum = 0
  let fibSeq = [1]
  let keepPushing = true

  while ( keepPushing ) {
    let lastNum = fibSeq.slice(-1)[0]
    let secondLastNum = fibSeq.slice(-2, -1)[0]
    
    if ( secondLastNum === undefined ) {
      nextNum = 1
    }
    else {
      nextNum = lastNum + secondLastNum
    }

    keepPushing = nextNum <= num

    if ( keepPushing ) {
      fibSeq.push(nextNum)
    }
  }

  let oddNums = fibSeq.filter(n => n % 2 === 1)
  let oddFibSum = oddNums.reduce((sum, val) => sum + val)
  
  console.log(oddFibSum)
  return oddFibSum
}

sumFibs(1000);
