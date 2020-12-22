--
-- To compile:
-- elm make src/Main.elm --output=index.js
--
module Main exposing (..)


-- IMPORTS

import Browser
import Html exposing (..)
import Html.Attributes exposing (type_, value, class, style, selected)
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

selectDefault =
  "---"


-- MODEL

type alias Model =
  { members : List Member
  , ageField : String
  , relationshipField : String
  , smokerField : Bool
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
    , relationshipField = selectDefault
    , smokerField = False
    , isValidMember = None
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
    SelectRelationship selectedOption ->
      ({ model | relationshipField = selectedOption }, Cmd.none)
    ToggleSmokes toggle ->
      ({ model | smokerField = toggleSmokerField model.smokerField }, Cmd.none)
    AddMember ->
      (resetForm (appendMember { model | isValidMember = validateMember model }), Cmd.none)
    DeleteMember ->
      (model, Cmd.none)
    SubmitHousehold ->
      (model, Cmd.none)

toggleSmokerField : Bool -> Bool
toggleSmokerField oldValue =
  not oldValue

validateMember : Model -> MemberValidator
validateMember model =
  let
    memberAge = Maybe.withDefault 0 (String.toInt model.ageField)
  in
    if not (memberAge > 0) then
      Error "Age must be number greater than 0."
    else if not (List.member model.relationshipField memberRelationships) then
      Error "Please select a valid relationship"
    else
      Ok

appendMember : Model -> Model
appendMember model =
  let
    newMember = { age = Maybe.withDefault 0 (String.toInt model.ageField)
                , relationship = model.relationshipField
                , smokes = model.smokerField
                }
  in
    case model.isValidMember of
      Ok ->
        { model | members = model.members ++ [ newMember ] }
      Error message ->
        model
      None ->
        model

resetForm : Model -> Model
resetForm model =
  case model.isValidMember of
    Ok ->
      { model | ageField = "", relationshipField = selectDefault, smokerField = False }
    Error message ->
      model
    None ->
      model


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
        , viewSelectOptions "Relationship" memberRelationships model.relationshipField SelectRelationship
        , viewInput "checkbox" "Smoker?" "true" ToggleSmokes
        , button [ class "add", onClick AddMember ] [ text "add" ]
        , button [ type_ "submit", onClick SubmitHousehold ] [ text "submit" ]
        ]
      ]
    , pre [ class "debug" ] [ text (boolToString model.smokerField) ]
    ]

boolToString : Bool -> String
boolToString boolValue =
  case boolValue of
    True ->
      "true"
    False ->
      "false"

viewMembersList : List Member -> Html msg
viewMembersList members =
  div [] (List.map memberToListItem members)

memberToListItem : Member -> Html msg
memberToListItem member =
  let
    memberRel = member.relationship
    memberAge = String.fromInt member.age
    memberSmoker = if member.smokes then "smoker" else "non-smoker"
  in
    li [ ] [ text (memberRel ++ " is a " ++ memberAge ++ " year-old " ++ memberSmoker ) ]

viewInput : String -> String -> String -> (String -> msg) -> Html msg
viewInput inputType labelText val toMsg =
  div []
    [ label []
      [ span [] [ text labelText ]
      , input [ type_ inputType, value val, onInput toMsg ] []
      ]
    ]

viewSelectOptions : String -> List String -> String -> (String -> msg) -> Html msg
viewSelectOptions labelText optionList selectedOption toMsg =
  let
    headedOptions = selectDefault :: optionList
  in
    div []
      [ label []
        [ span [] [ text labelText ]
        , select [ onInput toMsg ] (List.map (listToOptions selectedOption) headedOptions)
        ]
      ]

listToOptions : String -> String -> Html msg
listToOptions selectedOption optionValue =
  -- Source: https://www.reddit.com/r/elm/comments/4z4twe/in_a_select_element_how_do_i_designate_the/d6swmtc/
  let
    isSelected = optionValue == selectedOption
  in
    option [ value optionValue, selected isSelected ] [ text optionValue ]

viewMemberValidation : Model -> Html msg
viewMemberValidation model =
  case model.isValidMember of
    Ok ->
      div [ style "color" "green" ] [ text "OK" ]
    Error message ->
      div [ style "color" "red" ] [ text message ]
    None ->
      div [] [ text "Please enter a household member."]
