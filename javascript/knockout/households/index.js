// your code goes here ...
function HouseholdMember(age, relationship, smokes) {
  let member = this

  member.age = age
  member.relationship = relationship
  member.smokes = smokes

  member.asListItem = ko.computed(function() {
    const smokingIcon = '🚬'
    const noSmokingIcon = '🚭'
    const smokesIcon = member.smokes ? smokingIcon : noSmokingIcon
    return `${member.relationship}: ${member.age} ${smokesIcon}`
  })
}

function HouseholdsViewModel() {
  let model = this

  model.validRelationships = ['self', 'spouse', 'child', 'parent', 'grandparent', 'other']
  model.members = ko.observableArray([new HouseholdMember(40, 'self', false)])
  model.memberAge = ko.observable()
  model.memberRelationship = ko.observable()
  model.memberSmokes = ko.observable()
  model.debugText = ko.observable()
  model.toggleDebug = ko.observable(false)

  model.addMember = (el, event) => {
    let age = model.memberAge()
    let rel = model.memberRelationship()
    let smokes = model.memberSmokes()
    let newMember = new HouseholdMember(age, rel, smokes)

    model.members.push(newMember)
    model.resetForm()
  }

  model.removeMember = (member) => {
    if ( confirm("Remove this member?") ) {
      model.members.remove(member)
    }
  }

  model.submitForm = () => {
    let jsonMembers = ko.toJSON(model.members())

    model.debugText(jsonMembers)
    model.toggleDebug(true)
  }

  model.resetForm = () => {
    model.memberAge('')
    model.memberRelationship('')
    model.memberSmokes(false)
  }
}

ko.applyBindings(new HouseholdsViewModel());
