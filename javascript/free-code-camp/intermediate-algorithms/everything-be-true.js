function truthCheck(collection, pre) {
  let isTruthy = collection.every(obj => obj[pre])
  console.log(isTruthy)
  return isTruthy;
}

truthCheck([{"user": "Tinky-Winky", "sex": "male"}, {"user": "Dipsy", "sex": "male"}, {"user": "Laa-Laa", "sex": "female"}, {"user": "Po", "sex": "female"}], "sex");
