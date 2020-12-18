require 'spec_helper'
require_relative '../../app/models/household'

describe Household, type: :model do
  it { is_expected.to have_many(:household_members).class_name('HouseholdMember') }
end
