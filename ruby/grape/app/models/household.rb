class Household < ActiveRecord::Base
  has_many :household_members
  alias_attribute :members, :household_members

  # rubocop: disable Metrics/AbcSize
  def self.create_random(options={})
    size = options[:size] || rand(1..6)

    # Create household
    household = Household.new

    # First member is self
    selfie = HouseholdMember.create_random(relationship: 'self')
    household.members << selfie

    # Remaining members are random
    member_pool = HouseholdMember::RELATIONSHIPS.clone - ['self']
    (1..size - 1).each do
      relation = member_pool.sample
      member = HouseholdMember.create_random(relationship: relation)
      household.members << member
      member_pool.delete relation if relation == 'spouse'
    end

    household.save!
    household
  end
  # rubocop: enable Metrics/AbcSize

  def size
    members.length
  end
end
