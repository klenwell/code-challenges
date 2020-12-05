var Person = function(firstAndLast) {
  // Only change code below this line
  // Complete the method below and implement the others similarly
  let firstName, lastName

  this.getFirstName = function() {
    return firstName
  }

  this.getLastName = function() {
    return lastName;
  }

  this.getFullName = function() {
    return [firstName, lastName].join(' ');
  };

  this.setFirstName = function(_firstName) {
    firstName = _firstName
  }

  this.setLastName = function(_lastName) {
    lastName = _lastName
  }

  this.setFullName = function(fullName) {
    let [_firstName, _lastName] = fullName.split(' ')
    this.setFirstName(_firstName)
    this.setLastName(_lastName)
  };

  this.setFullName(firstAndLast)
};

var bob = new Person('Bob Ross');
bob.setFirstName("Haskell")
console.log(bob.getFullName())
