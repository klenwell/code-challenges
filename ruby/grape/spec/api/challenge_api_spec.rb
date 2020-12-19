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
      context 'requested household exists' do
        let(:household) { Household.create_random }

        it 'return a household by id parameter' do
          get "/api/v1/households/#{household.id}"
          json_data = JSON.parse(last_response.body)

          expect(last_response.status).to eq 200
          expect(json_data['household']['id']).to eq(household.id)
        end
      end

      context 'requested household does not exist' do
        it 'return a household by id parameter' do
          # Arrange
          expected_error = "Couldn't find Household with 'id'=0"

          # Act
          get "/api/v1/households/0"

          # Assert
          expect(last_response.status).to eq 404
          expect(JSON.parse(last_response.body)).to eq({ 'error' => expected_error })
        end
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
