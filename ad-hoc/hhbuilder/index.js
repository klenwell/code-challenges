// your code goes here ...
const form = document.getElementsByTagName('form')[0]
const ageField = form.querySelector("form input[name='age']")
const debugBlock = document.querySelector('pre.debug')

initHHBuilder()

// Helper Methods
function initHHBuilder () {
  console.debug(form, ageField, debugBlock)
  initFormHandler()
}

function initFormHandler () {
  form.addEventListener('submit', function (event) {
    console.debug(event)
    event.preventDefault()

    const formJson = formToJson(form)
    debugBlock.innerHTML = formJson
    debugBlock.style.display = 'block'
  })
}

function formToJson (formElement) {
  const formData = new FormData(formElement)
  return JSON.stringify(Object.fromEntries(formData.entries()))
}
