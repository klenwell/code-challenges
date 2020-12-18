class CreateHouseholds < ActiveRecord::Migration[6.0]
  def change
    # rubocop: disable Style/SymbolProc
    create_table :households do |t|
      t.timestamps
    end
    # rubocop: enable Style/SymbolProc
  end
end
