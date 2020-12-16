// your code goes here ...
function HouseholdMember (age, relationship, smokes) {
  const member = this

  member.age = age
  member.relationship = relationship
  member.smokes = smokes

  member.asListItem = ko.computed(() => {
    const smokingIcon = '🚬'
    const noSmokingIcon = '🚭'
    const smokesIcon = member.smokes ? smokingIcon : noSmokingIcon
    return `${member.relationship}: ${member.age} ${smokesIcon}`
  })
}

function HouseholdsViewModel () {
  const vm = this

  vm.validRelationships = ['self', 'spouse', 'child', 'parent', 'grandparent', 'other']
  vm.members = ko.observableArray([new HouseholdMember(40, 'self', false)])
  vm.memberAge = ko.observable().extend({ required: true, min: 1 })
  vm.memberRelationship = ko.observable().extend({ required: true })
  vm.memberSmokes = ko.observable()
  vm.debugText = ko.observable()
  vm.toggleDebug = ko.observable(false)

  vm.addMember = (el, event) => {
    if (!vm.isValid()) {
      vm.displayErrors()
      return
    }

    const age = vm.memberAge()
    const rel = vm.memberRelationship()
    const smokes = vm.memberSmokes()
    const newMember = new HouseholdMember(age, rel, smokes)

    vm.members.push(newMember)
    vm.resetForm()
  }

  vm.removeMember = (member) => {
    if (confirm('Remove this member?')) {
      vm.members.remove(member)
    }
  }

  vm.submitForm = () => {
    const jsonMembers = ko.toJSON(vm.members())

    vm.debugText(jsonMembers)
    vm.toggleDebug(true)
  }

  vm.resetForm = () => {
    vm.memberAge('')
    vm.memberRelationship('')
    vm.memberSmokes(false)
    vm.clearErrors()
  }

  // Knockout-Validation: https://github.com/Knockout-Contrib/Knockout-Validation/wiki
  vm.validation = ko.validation.group(vm)
  vm.errors = () => { return vm.validation() }
  vm.isValid = () => { return vm.errors().length === 0 }
  vm.displayErrors = () => { vm.validation.showAllMessages() }
  vm.clearErrors = () => { vm.validation.showAllMessages(false) }
}

ko.validation.init()
ko.applyBindings(new HouseholdsViewModel())
