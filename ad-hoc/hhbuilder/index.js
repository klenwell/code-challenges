// your code goes here ...
// Models
class Person {
  constructor (age, relationship, smokes) {
    this.age = age
    this.relationship = relationship
    this.smokes = smokes === 'on'
  }

  // Static Methods
  static fromForm (form) {
    const formData = new FormData(personForm)
    const personData = Object.fromEntries(formData.entries())
    return new Person(personData.age, personData.rel, personData.smoker)
  }

  // Methods
  ageIsValid () {
    return parseInt(this.age) > 0
  }

  relationshipIsValid () {
    return validRelations.includes(this.relationship)
  }

  isValid () {
    return this.ageIsValid() && this.relationshipIsValid()
  }

  toJson () {
    return {
      age: this.age,
      relationship: this.relationship,
      smokes: this.smokes
    }
  }
}

class Household {
  constructor () {
    this.people = []
  }

  // Methods
  addPerson (person) {
    this.people.push(person)
  }

  toJson () {
    return this.people.map(person => person.toJson())
  }
}

// Constants
const theHousehold = new Household()
const personForm = document.getElementsByTagName('form')[0]
const addButton = personForm.querySelector('button.add')
const submitButton = personForm.querySelector("button[type='submit']")
const householdList = document.querySelector('ol.household')
const debugBlock = document.querySelector('pre.debug')
const validRelations = ['self', 'spouse', 'child', 'parent', 'grandparent', 'other']

// Helper Methods
function initHHBuilder () {
  initFormHandler()
  initAddButtonHandler()
  initSubmitButtonHandler()
  personForm.reset()
}

function initFormHandler () {
  personForm.addEventListener('submit', function (event) {
    event.preventDefault()
  })
}

function initAddButtonHandler () {
  addButton.addEventListener('click', function (event) {
    const person = Person.fromForm(personForm)

    if (person.isValid()) {
      theHousehold.addPerson(person)
      renderHouseholdList(theHousehold)
      updateDebugBlock('person added to household')
      personForm.reset()
    } else {
      updateDebugBlock(buildErrorMessage(person))
    }
  })
}

function initSubmitButtonHandler () {
  submitButton.addEventListener('click', function (event) {
    console.debug('submitButton', event, theHousehold.toJson())
    updateDebugBlock(JSON.stringify(theHousehold.toJson()))
  })
}

function renderHouseholdList (household) {
  console.debug('renderHouseholdList', household, householdList)
  // Rebuild from scratch
  // Source: https://stackoverflow.com/questions/3955229
  while (householdList.firstChild) { householdList.firstChild.remove() }
  console.debug(householdList)

  household.people.forEach(function (person) {
    const li = document.createElement('li')
    const smokingIcon = '🚬'
    const noSmokingIcon = '🚭'
    const smokes = person.smokes ? smokingIcon : noSmokingIcon

    li.innerHTML = `${person.relationship}: ${person.age} ${smokes}`
    householdList.appendChild(li)
  })

  return householdList
}

function buildErrorMessage (person) {
  const messages = ['Form errors:']

  if (!person.ageIsValid()) {
    messages.push('Age is required and > 0')
  }

  if (!person.relationshipIsValid()) {
    messages.push('relationship is required')
  }

  return messages.join('\r\n')
}

function updateDebugBlock (message) {
  debugBlock.style.display = 'block'
  debugBlock.innerHTML = message
}

// Main
initHHBuilder()
