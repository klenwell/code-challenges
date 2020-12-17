require_relative '../../api/challenge_api'
require 'spec_helper'

describe Challenge::API do
  include Rack::Test::Methods

  def app
    Challenge::API
  end

  describe 'ping' do
    it 'returns pongs' do
      get '/api/v1/ping'
      expect(last_response.status).to eq(200)
      expect(JSON.parse(last_response.body)).to eq({ 'ping' => 'pong' })
    end
  end

  describe 'households' do
  end
end
