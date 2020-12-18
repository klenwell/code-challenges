require_relative '../../api/challenge_api'
require 'spec_helper'

# rubocop: disable Metrics/BlockLength
describe Challenge::API do
  include Rack::Test::Methods

  def app
    Challenge::API
  end

  describe 'GET /api/v1/ping' do
    it 'returns pong' do
      get '/api/v1/ping'
      expect(last_response.status).to eq 200
      expect(JSON.parse(last_response.body)).to eq({ 'ping' => 'pong' })
    end
  end

  describe 'households' do
    describe 'POST /api/v1/households' do
      it 'creates a new household' do
        members = []
        post '/api/v1/households', members.to_json, 'CONTENT_TYPE' => 'application/json'
        expect(last_response.status).to eq 201
      end
    end

    describe 'GET /api/v1/households/' do
      it 'return a household by id parameter' do
        household_id = 1
        get "/api/v1/households/#{household_id}"
        expect(last_response.status).to eq 200
      end
    end

    describe 'GET /api/v1/households/random' do
      let!(:response) do
        get "/api/v1/households/random"
        last_response
      end
      let(:json_data) { JSON.parse(last_response.body) }

      it { expect(response.status).to eq 200 }
      it { expect(json_data.keys).to include 'household' }
      it { expect(json_data.keys).to include 'members' }
      it { expect(json_data['members'].length).to be >= 1 }
    end
  end
end
# rubocop: enable Metrics/BlockLength
