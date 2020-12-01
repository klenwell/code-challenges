# O365 Activity

## Challenge
This wasn't for a job. It was a request from my sister who works as an independent consultant. She said one of her pain points is keeping up with client billing. She has to manually sift through her email, calendar, and Team messages to reconstruct her billing history. She said a script that could collect these activities for the past week or so and dump them in a CSV file for her review would be very helpful.

The code was a proof-of-concept to see if I could programmatically collect the data and produce a simple CSV.

## Result
I successfully built a command-line script using the [Python O365 library](https://github.com/O365/python-o365) to interact with the [Microsoft Graph REST API](https://docs.microsoft.com/en-us/graph/api/overview?view=graph-rest-1.0). My sister is not a programmer and uses Microsoft (obviously) so expecting her to run this script herself, while a possibility, is not ideal.

To authenticate, the script prints a URL to the console which you open in your browser, authorize the app to accesss your account, and then get back another URL that you paste back to get an auth token. My sister and I tried to do this remotely for her account by pasting URLs back and forth but we got a CSRF error.

So next step is to build a simple web app that she can use directly.
