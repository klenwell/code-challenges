# Knockout Households

This is a code challenge is based on the [Ad Hoc](https://homework.adhoc.team/) hhbuilder code challenge:

- https://github.com/klenwell/code-challenges/tree/main/ad-hoc/hhbuilder

I have adapted it to require [Knockout.js](https://knockoutjs.com/) as a way to introduce myself to that framework.

## Task

You have been given an HTML page with a form and a placeholder for displaying a household.

In the given index.js file, replace the "Your code goes here" comment with JavaScript that can:

- Validate data entry (age is required and > 0, relationship is required)
- Add people to a growing household list
- Reset the entry form after each addition
- Remove a previously added person from the list
- Display the household list in the HTML as it is modified
- Serialize the household as JSON upon form submission as a fake trip to the server

## Additional Requirements

- You can modify the index.html file but try to keep changes minimal.
- You must write JavaScript using the Knockout.js framework.
- The display of the household list is up to you.
- On submission, put the serialized JSON in the provided "debug" DOM element and display that element.
- After submission, the user should be able to make changes and submit the household again.
- You don't need to add validations around anything other than the age and relationship requirements described above. It's ok for someone to add 35 parents.

The focus here is on the quality of your JavaScript, not the beauty of your design. The controls you add around viewing and deleting household members should be usable but need not be much to look at.

## My Solution
To run it, I simply paste the file path in my browser, like so:

- file:///home/klenwell/projects/code-challenges/javascript/knockout/households/index.html
