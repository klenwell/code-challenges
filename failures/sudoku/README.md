# Sudoku Failure

## Challenge
To do the challenge yourself, remove the `sudoku_solver.py` file and open the `sudoku.py` file.

This was presented in a technical interview by a startup based out of the Midwest building a logistic/shipping platform using Ruby. They allowed you to choose your language. I picked Python because I had been doing more coding in it recently and am generally more comfortable with it for one-off stuff.

I found the challenge odd as the hiring company, as the first step in the hiring process, had already given me a take-home challenge that was inspired by a real business problem. I was hoping the technical interview would consist of reviewing that code and discussing some possible improvements.

 When I saw what I was actually expected to do, I groaned inside. I've never done sudoku before. Fortunately, the tests defined the interface and process. The interviewer also explained the rules of sudoku. It was open book, or open browser.

I was given about an hour to complete the challenge.

## Failure
At the end of the interview, the tests were not passing. It turned out I was very close. With an extra 15 minutes or so (after the interview), I had them all passing.

I had the basic code flow worked out fairly quickly. Most the time was wasted parsing the values list representing the board and dealing with off-by-one errors.

I felt it was a bit uncharitable to reject me based on this challenge. I thought it demonstrated the kind of basic proficiency with code and problem-solving that you're usually looking for with these kinds of tests. I'm sure there are more efficient ways to parse the board and neater ways to solve the problem. If interested in that, you can probably find them here:

- https://norvig.com/sudoku.html
