--
-- To compile:
-- elm make src/Flags.elm --output=javascript/flags.js
--
module Flags exposing (..)


import Browser
import Html exposing (Html, text, span, div)
import Time


-- MAIN

main : Program Int Model Msg
main =
  Browser.element
    { init = init
    , view = view
    , update = update
    , subscriptions = subscriptions
    }


-- MODEL

type alias Model = { currentTime : Int }

init : Int -> ( Model, Cmd Msg )
init currentTime =
  ( { currentTime = currentTime }
  , Cmd.none
  )


-- UPDATE

type Msg = NoOp

update : Msg -> Model -> ( Model, Cmd Msg )
update _ model =
  ( model, Cmd.none )


-- VIEW

view : Model -> Html Msg
view model =
  let
    loadTime = Time.millisToPosix model.currentTime
    hour   = String.fromInt (Time.toHour   Time.utc loadTime)
    minute = String.fromInt (Time.toMinute Time.utc loadTime)
    second = String.fromInt (Time.toSecond Time.utc loadTime)
  in
  div []
  [ span [] [ text "Time at page load:" ]
  , span [] [ text (hour ++ ":" ++ minute ++ ":" ++ second) ]
  ]


-- SUBSCRIPTIONS

subscriptions : Model -> Sub Msg
subscriptions _ =
  Sub.none
