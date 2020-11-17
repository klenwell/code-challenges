// your code goes here ...
// Constants
const personForm = document.getElementsByTagName('form')[0]
const addButton = personForm.querySelector("button.add")
const submitButton = personForm.querySelector("button[type='submit']")
const ageField = personForm.querySelector("input[name='age']")
const householdList = document.querySelector('ol.household')
const debugBlock = document.querySelector('pre.debug')


// Helper Methods
function initHHBuilder () {
  initFormHandler()
  initAddButtonHandler()
  initSubmitButtonHandler()
}

function initFormHandler () {
  personForm.addEventListener('submit', function() {
    event.preventDefault()
  });
}

function initAddButtonHandler () {
  addButton.addEventListener('click', function() {
    const formData = new FormData(personForm)
    const person = formDataToPerson(formData);

    if ( person.isValid() ) {
      addPersonToList(person);
    }
  });
}

function initSubmitButtonHandler () {
  submitButton.addEventListener('click', function() {
    console.debug('submitButton', event)
    const formJson = formToJson(personForm)
    debugBlock.innerHTML = JSON.stringify(formJson)
    debugBlock.style.display = 'block'
  });
}

function addPersonToList(person) {
  console.debug('addPersonToList', person);

  let li = document.createElement("li");
  let smoking_icon = '🚬'
  let no_smoking_icon = '🚭'
  let smokes = person.smoker === 'on' ? smoking_icon : no_smoking_icon;
  li.innerHTML = `${person.rel}: ${person.age} ${smokes}`
  householdList.appendChild(li);
  return li
}

function formDataToPerson(formData) {
  // Source: https://stackoverflow.com/a/55874235/1093087
  let person = Object.fromEntries(formData.entries())

  person.isValid = function() {
    return true;
  }

  return person
}


// Main
initHHBuilder()
