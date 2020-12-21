require 'spec_helper'
require_relative '../../app/models/household_member'

# rubocop: disable Metrics/BlockLength
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

  describe '.random' do
    context 'without parameters' do
      it 'will create a random member' do
        rando = HouseholdMember.create_random
        expect(rando).to be_instance_of HouseholdMember
        expect(described_class::RELATIONSHIPS).to include rando.relationship
        expect(rando.household).to be_nil
      end
    end

    context 'with parameters' do
      it 'will create a random member with random attrs' do
        age = 25
        smokes = true
        rando = HouseholdMember.create_random(age: age, smokes: smokes)

        expect(rando.age).to eq(age)
        expect(rando.smokes).to eq(smokes)
      end
    end
  end
end
# rubocop: enable Metrics/BlockLength
