--
-- To compile:
-- elm make src/Main.elm --output=index.js
--
module Main exposing (..)


-- IMPORTS

import Browser
import Html exposing (..)
import Html.Attributes exposing ( type_, value, class, style )
import Html.Events exposing (onClick, onInput)


-- MAIN

main =
  Browser.element
    { init = init
    , update = update
    , subscriptions = subscriptions
    , view = view
    }

memberRelationships =
  ["self", "spouse", "child", "parent", "grandparent", "other"]


-- MODEL

type alias Model =
  { members : List Member
  , ageField : String
  , relationship : String
  , smokes: Bool
  , isValidMember: MemberValidator
  }

type alias Member =
  { age : Int
  , relationship : String
  , smokes : Bool
  }

type MemberValidator
  = None
  | Ok
  | Error String

init : () -> (Model, Cmd Msg)
init _ =
  ( { members = []
    , ageField = ""
    , relationship = ""
    , smokes = False
    , isValidMember = Ok
    }
  , Cmd.none
  )


-- UPDATE

type Msg
  = InputAge String
  | SelectRelationship String
  | ToggleSmokes String
  | AddMember
  | DeleteMember
  | SubmitHousehold

update : Msg -> Model -> (Model, Cmd Msg)
update msg model =
  case msg of
    InputAge age ->
      ({ model | ageField = age }, Cmd.none)
    SelectRelationship rel ->
      (model, Cmd.none)
    ToggleSmokes smokes ->
      (model, Cmd.none)
    AddMember ->
      ({ model | isValidMember = validateMember model }, Cmd.none)
    DeleteMember ->
      (model, Cmd.none)
    SubmitHousehold ->
      (model, Cmd.none)

validateMember : Model -> MemberValidator
validateMember model =
  let
    memberAge = Maybe.withDefault 0 (String.toInt model.ageField)
  in
    if not (memberAge > 0) then
      Error "Age must be number greater than 0."
    else if not (List.member model.relationship memberRelationships) then
      Error "Please select a valid relationship"
    else
      Ok


-- SUBSCRIPTIONS

subscriptions : Model -> Sub Msg
subscriptions model =
  Sub.none


-- VIEW

view : Model -> Html Msg
view model =
  div []
    [ h1 [] [ text "Household Builder" ]
    , div [ class "builder" ]
      [ ol [ class "household" ] [ viewMembersList model.members ]
      , div []
        [ viewMemberValidation model
        , viewInput "text" "Age" model.ageField InputAge
        , viewSelectOptions "Relationship"
        , viewInput "checkbox" "Smoker?" "true" ToggleSmokes
        , button [ class "add", onClick AddMember ] [ text "add" ]
        , button [ type_ "submit", onClick SubmitHousehold ] [ text "submit" ]
        ]
      ]
    , pre [ class "debug" ] [ text "" ]
    ]

viewMembersList : List Member -> Html msg
viewMembersList members =
  div [] [ text "TODO: viewMembersList" ]

viewInput : String -> String -> String -> (String -> msg) -> Html msg
viewInput inputType labelText val toMsg =
  div []
    [ label []
      [ span [] [ text labelText ]
      , input [ type_ inputType, value val, onInput toMsg ] []
      ]
    ]

viewSelectOptions : String -> Html msg
viewSelectOptions labelText =
  div [] [ text ("TODO: " ++ labelText) ]

viewMemberValidation : Model -> Html msg
viewMemberValidation model =
  case model.isValidMember of
    Ok ->
      div [ style "color" "green" ] [ text "OK" ]
    Error message ->
      div [ style "color" "red" ] [ text message ]
    None ->
      div [] [ text "Please enter a household member."]
