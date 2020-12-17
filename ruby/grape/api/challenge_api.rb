module Challenge
  class API < Grape::API
    prefix :api
    version 'v1'
    format :json

    # GET /api/v1/ping
    get :ping do
      { ping: 'pong' }
    end
  end
end
