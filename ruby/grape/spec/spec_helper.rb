# frozen_string_literal: true

# Source: https://github.com/ruby-grape/grape/blob/master/spec/spec_helper.rb
$LOAD_PATH.unshift(File.dirname(__FILE__))
$LOAD_PATH.unshift(File.join(File.dirname(__FILE__), '..', 'api'))

require "rack/test"
require 'grape'

RSpec.configure do |config|
  config.include Rack::Test::Methods
  config.raise_errors_for_deprecations!
  config.filter_run_when_matching :focus
  config.warnings = true

  config.before(:each) { Grape::Util::InheritableSetting.reset_global! }

  # Enable flags like --only-failures and --next-failure
  config.example_status_persistence_file_path = '.rspec_status'
end
