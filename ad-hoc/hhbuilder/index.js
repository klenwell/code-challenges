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

  // Instance Methods
  removePerson (person) {
    this.people = this.people.filter(member => member !== person)
    return this.people
  }

  toJson () {
    return this.people.map(person => person.toJson())
  }
}

// Constants
const theHousehold = new Household()
const personForm = document.getElementsByTagName('form')[0]
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
  const addButton = personForm.querySelector('button.add')

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
  const submitButton = personForm.querySelector("button[type='submit']")

  submitButton.addEventListener('click', function (event) {
    updateDebugBlock(JSON.stringify(theHousehold.toJson()))
  })
}

function renderHouseholdList (household) {
  // Rebuild from scratch
  // Source: https://stackoverflow.com/questions/3955229
  const householdList = document.querySelector('ol.household')

  while (householdList.firstChild) { householdList.firstChild.remove() }

  household.people.forEach(function (person) {
    const li = buildHouseholdListItem(household, person)
    householdList.appendChild(li)
  })

  return householdList
}

function buildHouseholdListItem (household, person) {
  const smokingIcon = '🚬'
  const noSmokingIcon = '🚭'
  const li = document.createElement('li')

  const personSpan = document.createElement('span')
  const smokes = person.smokes ? smokingIcon : noSmokingIcon
  personSpan.innerHTML = `${person.relationship}: ${person.age} ${smokes}`
  li.appendChild(personSpan)

  const deleteButton = buildDeleteButton(li, household, person)
  li.appendChild(deleteButton)

  return li
}

function buildDeleteButton (li, household, person) {
  const button = document.createElement('button')
  button.appendChild(document.createTextNode('x'))

  button.addEventListener('click', function (event) {
    household.removePerson(person)
    li.remove()
    updateDebugBlock('removed person from household')
  })

  return button
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
  const debugBlock = document.querySelector('pre.debug')
  debugBlock.style.display = 'block'
  debugBlock.innerHTML = message
}

// Main
initHHBuilder()
