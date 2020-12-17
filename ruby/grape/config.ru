# https://github.com/ruby-grape/grape#alongside-sinatra-or-other-frameworks
require 'grape'

class PingApi < Grape::API
  get :ping do
    { ping: 'pong' }
  end
end

run PingApi
