require 'spec_helper'
require_relative '../../app/models/household_member'

describe HouseholdMember, type: :model do
  it { is_expected.to be_a HouseholdMember }
end
