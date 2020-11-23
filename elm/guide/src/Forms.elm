--
-- To compile:
-- elm make src/Forms.elm --output=forms.js
--
module Forms exposing (..)

import Browser
import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (onInput)
import Char exposing (isDigit, isUpper, isLower)



-- MAIN


main =
  Browser.sandbox { init = init, update = update, view = view }



-- MODEL


type alias Model =
  { name : String
  , password : String
  , passwordAgain : String
  }


init : Model
init =
  Model "" "" ""



-- UPDATE


type Msg
  = Name String
  | Password String
  | PasswordAgain String


update : Msg -> Model -> Model
update msg model =
  case msg of
    Name name ->
      { model | name = name }

    Password password ->
      { model | password = password }

    PasswordAgain password ->
      { model | passwordAgain = password }



-- VIEW


view : Model -> Html Msg
view model =
  div []
    [ viewInput "text" "Name" model.name Name
    , viewInput "password" "Password" model.password Password
    , viewInput "password" "Re-enter Password" model.passwordAgain PasswordAgain
    , viewValidation model
    ]


viewInput : String -> String -> String -> (String -> msg) -> Html msg
viewInput t p v toMsg =
  input [ type_ t, placeholder p, value v, onInput toMsg ] []



viewValidation : Model -> Html msg
viewValidation model =
  if String.length model.password < 8 then
    div [ style "color" "red" ] [ text "Passwords must be at least 8 chars!" ]
  else if not (String.any isDigit model.password) then
    div [ style "color" "red" ] [ text "Password must contain at least one digit!" ]
  else if not (String.any isUpper model.password) then
    div [ style "color" "red" ] [ text "Password must contain at least one uppercase char!" ]
  else if not (String.any isLower model.password) then
    div [ style "color" "red" ] [ text "Password must contain at least one lowercase char!" ]
  else if model.password /= model.passwordAgain then
    div [ style "color" "red" ] [ text "Passwords do not match!" ]
  else
    div [ style "color" "green" ] [ text "OK" ]
