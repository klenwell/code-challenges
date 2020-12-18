require 'spec_helper'
require_relative '../../app/models/household_member'

describe HouseholdMember, type: :model do
  describe 'associations' do
    it { is_expected.to belong_to(:household).class_name('Household') }
  end

  describe '#validations' do
    it { is_expected.to validate_presence_of(:age) }
    it { is_expected.to validate_numericality_of(:age).is_greater_than(0) }
    it { is_expected.to validate_presence_of(:relationship) }
    it {
      is_expected.to validate_inclusion_of(:relationship)
        .in_array(described_class::RELATIONSHIPS)
    }
  end

  describe '#smokes?' do
    subject(:smoker) { HouseholdMember.new(smokes: true) }

    it { expect(smoker.smokes?).to be(true) }
  end
end
