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

  const validRelationships = ['self', 'spouse', 'child', 'parent', 'grandparent', 'other']

  model.members = ko.observableArray([
    new HouseholdMember(40, validRelationships[0], false)
  ])

  model.addMember = () => { console.log("TODO: addMember") }

  model.submit = () => { console.log("TODO: submit") }
}

ko.applyBindings(new HouseholdsViewModel());
