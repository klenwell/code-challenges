require 'spec_helper'
require_relative '../../app/models/household'

describe Household, type: :model do
  it { is_expected.to have_many(:household_members).class_name('HouseholdMember') }

  describe '.random' do
    context 'without specified size' do
      subject(:household) { Household.create_random }

      it { expect(household.size).to be_between(1, 6) }

      it 'expects one self per household ' do
        selves = household.members.select(&:self?).length
        expect(selves).to eq(1)
      end
    end
  end
end
