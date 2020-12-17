# https://github.com/ruby-grape/grape#alongside-sinatra-or-other-frameworks
require 'grape'
require_relative 'api/challenge_api'

run Challenge::API
