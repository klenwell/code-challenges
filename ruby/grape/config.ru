# https://github.com/ruby-grape/grape#alongside-sinatra-or-other-frameworks
root_path = File.dirname(__FILE__)

require 'grape'
require 'active_record'

# Load API and models
Dir["#{root_path}/api/*.rb"].sort.each { |f| require f }
Dir["#{root_path}/app/models/**/*.rb"].sort.each { |f| require f }

# Connect to test database: https://stackoverflow.com/q/14519951/1093087
# TODO: dynamic environment support
# Set env to *not* development to disable exceptions: https://stackoverflow.com/a/51741710/1093087
env = 'development'
db_config_file = "#{root_path}/db/config.yml"
db_config = YAML.safe_load(File.read(db_config_file), [], [], true)
ActiveRecord::Base.establish_connection(db_config[env])

# API runs as an app
run Challenge::API
