require_relative '../../api/challenge_api'
require 'spec_helper'

# rubocop: disable Metrics/BlockLength
describe Challenge::API do
  include Rack::Test::Methods

  def app
    Challenge::API
  end

  describe 'ping' do
    it 'returns pongs' do
      get '/api/v1/ping'
      expect(last_response.status).to eq 200
      expect(JSON.parse(last_response.body)).to eq({ 'ping' => 'pong' })
    end
  end

  describe 'households' do
    describe 'create' do
      it 'creates a new household' do
        members = []
        post '/api/v1/households', members.to_json, 'CONTENT_TYPE' => 'application/json'
        expect(last_response.status).to eq 201
      end
    end

    describe 'get' do
      it 'return a household by id parameter' do
        household_id = 1
        get "/api/v1/households/#{household_id}"
        expect(last_response.status).to eq 200
      end
    end

    describe 'random' do
      it 'generates and returns a random household' do
        get "/api/v1/households/random"
        expect(last_response.status).to eq 200
      end
    end
  end
end
# rubocop: enable Metrics/BlockLength
