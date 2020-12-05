function smallestCommons(arr) {
    let range = arrayToRange(arr)

    // https://stackoverflow.com/a/147539/1093087
    let scm = range.reduce((acc, val) => lcm(acc,val))

    console.log(scm)
    return scm
}

function arrayToRange(arr) {
  let range = []
  let sortedArray = arr.sort((a, b) => a < b ? -1 : a > b ? 1 : 0)
  let start = sortedArray[0]
  let end = sortedArray[1]

  for (let i=start; i<=end; i++) {
    range.push(i)
  }

  return range
}

// Next 2 functions: https://stackoverflow.com/a/2641293/1093087
function gcd(a, b){
    // Euclidean algorithm
    var t;
    while (b != 0){
        t = b;
        b = a % b;
        a = t;
    }
    return a;
}

function lcm(a, b){
    return (a * b / gcd(a, b));
}


smallestCommons([1,13]);
