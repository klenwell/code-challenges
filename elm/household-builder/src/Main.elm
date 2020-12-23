--
-- To compile:
-- elm make src/Main.elm --output=index.js
--
module Main exposing (..)


-- IMPORTS

import Browser
import Html exposing (..)
import Html.Attributes exposing (type_, value, class, style, selected, checked)
import Html.Events exposing (onClick, onInput)
import Json.Encode as Encode


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
  , serializedHousehold: Encode.Value
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
    , serializedHousehold = Encode.string ""
    }
  , Cmd.none
  )


-- UPDATE

type Msg
  = InputAge String
  | SelectRelationship String
  | ToggleSmokes String
  | AddMember
  | DeleteMember Member
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
    DeleteMember member ->
      (removeMember model member, Cmd.none)
    SubmitHousehold ->
      ({ model | serializedHousehold = serializeHousehold model.members }, Cmd.none)

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

serializeHousehold : List Member -> Encode.Value
serializeHousehold memberList =
  Encode.list encodeMember memberList

encodeMember : Member -> Encode.Value
encodeMember member =
  Encode.object
    [ ( "age", Encode.int member.age )
    , ( "relationship", Encode.string member.relationship )
    , ( "smokes", Encode.bool member.smokes )
    ]

removeMember : Model -> Member -> Model
removeMember model member =
  let
    newMembers = List.filter (\m -> m /= member) model.members
  in
    { model | members = newMembers }


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
        , viewTextInput "Age" model.ageField InputAge
        , viewSelectOptions "Relationship" memberRelationships model.relationshipField SelectRelationship
        , viewCheckbox "Smoker?" model.smokerField ToggleSmokes
        , button [ class "add", onClick AddMember ] [ text "add" ]
        , button [ type_ "submit", onClick SubmitHousehold ] [ text "submit" ]
        ]
      ]
    , pre [ class "debug" ] [ text (Encode.encode 4 model.serializedHousehold) ]
    ]

viewMembersList : List Member -> Html Msg
viewMembersList members =
  div [] (List.map memberToListItem members)

memberToListItem : Member -> Html Msg
memberToListItem member =
  let
    relation = member.relationship
    age = String.fromInt member.age
    smoker = if member.smokes then "smoker" else "non-smoker"
    memberText = relation ++ " is a " ++ age ++ " year-old " ++ smoker
  in
    li []
      [ span [] [ text memberText ]
      , button [ class "delete", onClick (DeleteMember member) ] [ text "x" ]
      ]

viewTextInput : String -> String -> (String -> msg) -> Html msg
viewTextInput labelText val toMsg =
  div []
    [ label []
      [ span [] [ text labelText ]
      , input [ type_ "text", value val, onInput toMsg ] []
      ]
    ]

viewCheckbox : String -> Bool -> (String -> msg) -> Html msg
viewCheckbox labelText isChecked toMsg =
  div []
    [ label []
      [ span [] [ text labelText ]
      , input [ type_ "checkbox", checked isChecked, onInput toMsg ] []
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
