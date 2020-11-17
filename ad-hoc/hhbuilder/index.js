// your code goes here ...
// Constants
const personForm = document.getElementsByTagName('form')[0]
const addButton = personForm.querySelector('button.add')
const submitButton = personForm.querySelector("button[type='submit']")
const householdList = document.querySelector('ol.household')
const debugBlock = document.querySelector('pre.debug')

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
    const formData = new FormData(personForm)
    const person = formDataToPerson(formData)

    if (person.isValid) {
      addPersonToList(person)
      updateDebugBlock('person added to household')
      personForm.reset()
    } else {
      updateDebugBlock(buildErrorMessage(person))
    }
  })
}

function initSubmitButtonHandler () {
  submitButton.addEventListener('click', function (event) {
    console.debug('submitButton', event)
    const formData = new FormData(personForm)
    const formJson = Object.fromEntries(formData.entries())
    updateDebugBlock(JSON.stringify(formJson))
  })
}

function addPersonToList (person) {
  console.debug('addPersonToList', person)
  const li = document.createElement('li')
  const smokingIcon = '🚬'
  const noSmokingIcon = '🚭'
  const smokes = person.smoker === 'on' ? smokingIcon : noSmokingIcon

  li.innerHTML = `${person.rel}: ${person.age} ${smokes}`
  householdList.appendChild(li)
  return li
}

function formDataToPerson (formData) {
  // Source: https://stackoverflow.com/a/55874235/1093087
  const person = Object.fromEntries(formData.entries())
  person.ageIsValid = validateAge(person.age)
  person.relIsValid = validateRelationship(person.rel)
  person.isValid = person.ageIsValid && person.relIsValid
  return person
}

function validateAge (age) {
  return parseInt(age) > 0
}

function validateRelationship (relation) {
  const validRelations = ['self', 'spouse', 'child', 'parent', 'grandparent', 'other']
  return validRelations.includes(relation)
}

function buildErrorMessage (person) {
  const messages = ['Form errors:']

  if (!person.ageIsValid) {
    messages.push('Age is required and > 0')
  }

  if (!person.relIsValid) {
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
