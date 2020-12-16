// your code goes here ...
function HouseholdMember (age, relationship, smokes) {
  const member = this

  member.age = age
  member.relationship = relationship
  member.smokes = smokes

  member.asListItem = ko.computed(function () {
    const smokingIcon = '🚬'
    const noSmokingIcon = '🚭'
    const smokesIcon = member.smokes ? smokingIcon : noSmokingIcon
    return `${member.relationship}: ${member.age} ${smokesIcon}`
  })
}

function HouseholdsViewModel () {
  const model = this

  model.validRelationships = ['self', 'spouse', 'child', 'parent', 'grandparent', 'other']
  model.members = ko.observableArray([new HouseholdMember(40, 'self', false)])
  model.memberAge = ko.observable().extend({ required: true, min: 1 })
  model.memberRelationship = ko.observable().extend({ required: true })
  model.memberSmokes = ko.observable()
  model.debugText = ko.observable()
  model.toggleDebug = ko.observable(false)

  model.addMember = (el, event) => {
    if (!model.isValid()) {
      model.displayErrors()
      return
    }

    const age = model.memberAge()
    const rel = model.memberRelationship()
    const smokes = model.memberSmokes()
    const newMember = new HouseholdMember(age, rel, smokes)

    model.members.push(newMember)
    model.resetForm()
  }

  model.removeMember = (member) => {
    if (confirm('Remove this member?')) {
      model.members.remove(member)
    }
  }

  model.submitForm = () => {
    const jsonMembers = ko.toJSON(model.members())

    model.debugText(jsonMembers)
    model.toggleDebug(true)
  }

  model.resetForm = () => {
    model.memberAge('')
    model.memberRelationship('')
    model.memberSmokes(false)
    model.clearErrors()
  }

  // Knockout-Validation: https://github.com/Knockout-Contrib/Knockout-Validation/wiki
  model.validation = ko.validation.group(model)
  model.errors = () => { return model.validation() }
  model.isValid = () => { return model.errors().length === 0 }
  model.displayErrors = () => { model.validation.showAllMessages() }
  model.clearErrors = () => { model.validation.showAllMessages(false) }
}

ko.validation.init()
ko.applyBindings(new HouseholdsViewModel())
