class HouseholdMember < ActiveRecord::Base
  belongs_to :household

  RELATIONSHIPS = ['self', 'spouse', 'child', 'parent', 'grandparent', 'other'].freeze

  validates :age, presence: true, numericality: { greater_than: 0 }
  validates :relationship, presence: true, inclusion: { in: RELATIONSHIPS }
end
