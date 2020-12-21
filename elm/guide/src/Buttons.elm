--
-- To compile:
-- elm make src/Buttons.elm --output=buttons.js
--
module Buttons exposing (..)

import Browser
import Html exposing (Html, button, div, text)
import Html.Events exposing (onClick)



-- MAIN


main =
  Browser.sandbox { init = init, update = update, view = view }



-- MODEL

type alias Model = Int

init : Model
init =
  0


-- UPDATE

type Msg = Increment | Decrement | Reset | IncrementTen

update : Msg -> Model -> Model
update msg model =
  case msg of
    Increment ->
      model + 1

    Decrement ->
      model - 1

    IncrementTen ->
      model + 10

    Reset ->
      0


-- VIEW

view : Model -> Html Msg
view model =
  div []
    [ button [ onClick Decrement ] [ text "-" ]
    , div [] [ text (String.fromInt model) ]
    , button [ onClick Increment ] [ text "+" ]
    , div [] []
    , button [ onClick IncrementTen ] [ text "+10" ]
    , div [] []
    , button [ onClick Reset ] [ text "reset" ]
    ]
