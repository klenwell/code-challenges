--
-- To compile:
-- elm make src/TimeKeeper.elm --output=javascript/time_keeper.js
--
module TimeKeeper exposing (..)

import Browser
import Html exposing (..)
import Html.Events exposing (onClick)
import Task
import Time



-- MAIN


main =
  Browser.element
    { init = init
    , view = view
    , update = update
    , subscriptions = subscriptions
    }



-- MODEL


type alias Model =
  { zone : Time.Zone
  , time : Time.Posix
  , paused : Bool
  }


init : () -> (Model, Cmd Msg)
init _ =
  ( Model Time.utc (Time.millisToPosix 0) False
  , Task.perform AdjustTimeZone Time.here
  )



-- UPDATE


type Msg
  = Tick Time.Posix
  | AdjustTimeZone Time.Zone
  | Toggle



update : Msg -> Model -> (Model, Cmd Msg)
update msg model =
  case msg of
    Tick newTime ->
      ( { model | time = newTime }
      , Cmd.none
      )

    AdjustTimeZone newZone ->
      ( { model | zone = newZone }
      , Cmd.none
      )

    Toggle ->
      ( { model | paused = not model.paused }
      , Cmd.none
      )



-- SUBSCRIPTIONS


subscriptions : Model -> Sub Msg
subscriptions model =
    if model.paused
    then Sub.none
    else Time.every 1000 Tick



-- VIEW


view : Model -> Html Msg
view model =
  let
    hour   = String.fromInt (Time.toHour   model.zone model.time)
    minute = String.fromInt (Time.toMinute model.zone model.time)
    second = String.fromInt (Time.toSecond model.zone model.time)
    btnText =
      if model.paused then
        "Unpause"
      else
        "Pause"
  in
  div [] [
    h1 [] [ text (hour ++ ":" ++ minute ++ ":" ++ second) ],
    button [ onClick Toggle ] [ text btnText ]
  ]
