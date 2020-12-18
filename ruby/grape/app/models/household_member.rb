class HouseholdMember < ActiveRecord::Base
  belongs_to :household

  RELATIONSHIPS = ['self', 'spouse', 'child', 'parent', 'grandparent', 'other'].freeze

  validates :age, presence: true, numericality: { greater_than: 0 }
  validates :relationship, presence: true, inclusion: { in: RELATIONSHIPS }

  def self.random(options = {})
    member = HouseholdMember.new
    member.age = options[:age] || rand(1..80)
    member.relationship = options[:relationshp] || RELATIONSHIPS.sample
    member.smokes = options[:smokes] || [true, false].sample
    member.save!
    member
  end
end
