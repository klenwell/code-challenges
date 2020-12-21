--
-- To compile:
-- elm make src/Main.elm --output=index.js
--
module Main exposing (..)


-- IMPORTS

import Browser
import Html exposing (..)
import Html.Attributes exposing ( type_, value, class )
import Html.Events exposing (onClick, onInput)


-- MAIN

main =
  Browser.element
    { init = init
    , update = update
    , subscriptions = subscriptions
    , view = view
    }


-- MODEL

type alias Model =
  { members : List Member
  , age : Int
  , relationship : String
  , smokes: Bool
  }

type alias Member =
  { age : Int
  , relationship : String
  , smokes : Bool
  }

init : () -> (Model, Cmd Msg)
init _ =
  ( { members = []
    , age = 0
    , relationship = ""
    , smokes = False
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
      (model, Cmd.none)
    SelectRelationship rel ->
      (model, Cmd.none)
    ToggleSmokes smokes ->
      (model, Cmd.none)
    AddMember ->
      (model, Cmd.none)
    DeleteMember ->
      (model, Cmd.none)
    SubmitHousehold ->
      (model, Cmd.none)


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
      , form []
        [ viewInput "text" "Age" (String.fromInt model.age) InputAge
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
