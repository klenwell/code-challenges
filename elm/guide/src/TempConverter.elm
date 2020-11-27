--
-- To compile:
-- elm make src/TempConverter.elm --output=temp_converter.js
--
-- I wrote a little program here that converts from Celsius to Fahrenheit. Try
-- refactoring the view code in different ways:
--
-- - Can you put a red border around invalid input?
-- - Can you add more conversions? Fahrenheit to Celsius?
-- - Inches to Meters?
--
module TempConverter exposing (..)

import Browser
import Html exposing (Html, Attribute, span, input, text, div, h2)
import Html.Attributes exposing (..)
import Html.Events exposing (onInput)



-- MAIN


main =
  Browser.sandbox { init = init, update = update, view = view }



-- MODEL

type alias Model =
  { celsius : String
  , farenheit : String
  , inches : String
  , conversion : String
  }


init : Model
init =
  Model "" "" "" ""



-- UPDATE


type Msg
  = ConvertCelsius String
  | ConvertFahrenheit String
  | ConvertInches String

update : Msg -> Model -> Model
update msg model =
  case msg of
    ConvertCelsius newInput ->
      { model | celsius = newInput, conversion = convertCelsius newInput }
    ConvertFahrenheit newInput ->
      { model | farenheit = newInput, conversion = convertFahrenheit newInput }
    ConvertInches newInput ->
      { model | inches = newInput, conversion = convertInches newInput }

convertCelsius : String -> String
convertCelsius input =
  case String.toFloat input of
    Just celsius ->
      String.fromFloat (celsius * 1.8 + 32) ++ " °F"
    Nothing ->
      "???"

convertFahrenheit : String -> String
convertFahrenheit input =
    case String.toFloat input of
      Just fahrenheit ->
        String.fromFloat ((fahrenheit - 32) * 5 / 9) ++ " °C"
      Nothing ->
        "???"

convertInches : String -> String
convertInches input =
    case String.toFloat input of
      Just inches ->
        String.fromFloat (inches * 2.54) ++ " cm"
      Nothing ->
        "???"


-- VIEW


view : Model -> Html Msg
view model =
  div []
    [ viewInput model.celsius ConvertCelsius "°C"
    , viewInput model.farenheit ConvertFahrenheit "°F"
    , viewInput model.inches ConvertInches "inches"
    , viewOutput model.conversion
    ]

viewInput : String -> (String -> Msg) -> String -> Html Msg
viewInput userInput onInputMsg label =
  div []
    [ input [ value userInput, onInput onInputMsg, style "width" "40px"] []
    , text label
    ]

viewOutput : String -> Html Msg
viewOutput output =
  div []
    [ h2 []
      [ text "Conversion: "
      , span [] [ text output ]
      ]
    ]
