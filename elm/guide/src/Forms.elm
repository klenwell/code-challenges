--
-- To compile:
-- elm make src/Forms.elm --output=forms.js
--
module Forms exposing (..)

import Browser
import Html exposing (..)
import Html.Attributes exposing (..)
import Html.Events exposing (onInput, onClick)
import Char exposing (isDigit, isUpper, isLower)



-- MAIN


main =
  Browser.sandbox { init = init, update = update, view = view }



-- MODEL


type alias Model =
  { name : String
  , password : String
  , passwordAgain : String
  , validation : Validation
  }


init : Model
init =
  Model "" "" "" None


type Validation
  = None
  | Ok
  | Error String


-- Source: https://gist.github.com/moonlightdrive/86b5bcb57df87c45f468a13a326894ad#gistcomment-3089601
validateModel : Model -> Validation
validateModel model =
  let
    minLength = 8
  in
    if String.length model.name == 0 then
      Error "Please enter a name."
    else if String.length model.password < minLength then
      Error "Passwords must be at least 8 characters."
    else if not (String.any isDigit model.password) then
      Error "Password must contain at least one digit."
    else if not (String.any isUpper model.password) then
      Error "Password must contain at least one uppercase character."
    else if not (String.any isLower model.password) then
      Error "Password must contain at least one lowercase character."
    else if model.password /= model.passwordAgain then
      Error "Passwords do not match."
    else
      Ok




-- UPDATE


type Msg
  = Name String
  | Password String
  | PasswordAgain String
  | SubmitForm


update : Msg -> Model -> Model
update msg model =
  case msg of
    Name name ->
      { model | name = name }

    Password password ->
      { model | password = password }

    PasswordAgain password ->
      { model | passwordAgain = password }

    SubmitForm ->
      { model | validation = validateModel model }



-- VIEW


view : Model -> Html Msg
view model =
  div []
    [ viewInput "text" "Name" model.name Name
    , viewInput "password" "Password" model.password Password
    , viewInput "password" "Re-enter Password" model.passwordAgain PasswordAgain
    , button [ onClick SubmitForm ] [ text "Submit" ]
    , viewValidation model
    ]


viewInput : String -> String -> String -> (String -> msg) -> Html msg
viewInput t p v toMsg =
  input [ type_ t, placeholder p, value v, onInput toMsg ] []


viewValidation : Model -> Html msg
viewValidation model =
  case model.validation of
    Ok ->
      div [ style "color" "green" ] [ text "OK" ]
    Error message ->
      div [ style "color" "red" ] [ text message ]
    None ->
      div [] [ text "Please enter your information."]
