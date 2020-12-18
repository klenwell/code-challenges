class CreateHouseholdMembers < ActiveRecord::Migration[6.0]
  def change
    create_table :household_members do |t|
      t.belongs_to :household
      t.integer :age
      t.string :relationship
      t.boolean :smokes

      t.timestamps
    end
  end
end
