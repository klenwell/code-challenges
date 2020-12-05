function sumPrimes(num) {
  let primes = []

  for (let i=1; i<=num; i++) {
    if (isPrime(i)) {
      primes.push(i)
    }
  }

  let sum = primes.reduce((acc, val) => acc + val)

  console.log(sum)
  return sum;
}

// https://stackoverflow.com/a/40200710/1093087
function isPrime(num) {
  for (let i = 2, s = Math.sqrt(num); i <= s; i++)
    if(num % i === 0) return false; 
  return num > 1;
}

sumPrimes(10);
