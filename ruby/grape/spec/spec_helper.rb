# frozen_string_literal: true

# Source: https://github.com/ruby-grape/grape/blob/master/spec/spec_helper.rb
root_path = File.join(File.dirname(__FILE__), '..')

require "rack/test"
require 'grape'
require 'active_record'
require 'shoulda-matchers'

Dir["#{root_path}/app/models/**/*.rb"].each {|f| require f}
Dir["#{root_path}/api/*.rb"].each {|f| require f}

# Connect to test database: https://stackoverflow.com/q/14519951/1093087
# On safe_load args: https://stackoverflow.com/a/43767643/1093087
env = 'test'
db_config_file = "#{root_path}/db/config.yml"
db_config = YAML.safe_load(File.read(db_config_file), [], [], true)
ActiveRecord::Base.establish_connection(db_config[env])

RSpec.configure do |config|
  config.include Rack::Test::Methods
  config.raise_errors_for_deprecations!
  config.filter_run_when_matching :focus
  config.warnings = true

  config.before(:each) { Grape::Util::InheritableSetting.reset_global! }

  # Run specs in random order to surface order dependencies. If you find an
  # order dependency and want to debug it, you can fix the order by providing
  # the seed, which is printed after each run.
  #     --seed 1234
  config.order = "random"

  # Run each test inside a DB transaction
  config.around(:each) do |test|
    ActiveRecord::Base.transaction do
      test.run
      raise ActiveRecord::Rollback
    end
  end

  # Enable flags like --only-failures and --next-failure
  config.example_status_persistence_file_path = '.rspec_status'
end

# Source: https://github.com/thoughtbot/shoulda-matchers#non-rails-apps
Shoulda::Matchers.configure do |config|
  config.integrate do |with|
    with.test_framework :rspec

    # Keep as many of these lines as are necessary:
    with.library :active_record
    with.library :active_model
  end
end
