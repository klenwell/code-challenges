module Challenge
  class API < Grape::API
    prefix :api
    version 'v1'
    format :json

    # https://github.com/ruby-grape/grape#exception-handling
    rescue_from ActiveRecord::RecordNotFound do |e|
      error!(e, 404)
    end

    rescue_from :all

    resources :households do
      # POST /api/v1/households
      desc 'Create a household.'
      post do
        { post: 'TODO' }
      end

      # GET /api/v1/households/random
      desc 'Return a randomly generated household.'
      get :random do
        household = Household.create_random
        {
          household: household,
          members: household.members
        }
      end

      # GET /api/v1/households/:id
      desc 'Read a household.'
      params do
        requires :id, type: Integer, desc: 'Household ID.'
      end
      route_param :id do
        get do
          household = Household.find(params[:id])
          {
            household: household,
            members: household.members
          }
        end
      end
    end

    # GET /api/v1/ping
    get :ping do
      { ping: 'pong' }
    end
  end
end
