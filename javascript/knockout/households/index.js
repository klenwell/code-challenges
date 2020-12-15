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

  model.memberAge = ko.observable();
  model.memberRelationship = ko.observable();
  model.memberSmokes = ko.observable();
  model.members = ko.observableArray([new HouseholdMember(40, 'self', false)])

  model.addMember = () => {
    let age = model.memberAge()
    let rel = model.memberRelationship()
    let smokes = model.memberSmokes()
    let newMember = new HouseholdMember(age, rel, smokes)
    model.members.push(newMember)
  }

  model.submitForm = () => {
    console.log("TODO: submit", model.members())
  }
}

ko.applyBindings(new HouseholdsViewModel());
