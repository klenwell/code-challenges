class Household < ActiveRecord::Base
  has_many :household_members
end
