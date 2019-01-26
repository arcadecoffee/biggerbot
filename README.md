#1 BiggerBot
## Summary
This is a super simple SlackBot.  Really it is just an implementation of a couple of slash-commands intended to be attached to a Slack workspace.
This is written in Python 3 and uses Flask.
It can be deployed directly and run via `flask run` or the `run_gunicorn.sh` script or it can be deployed into serverlessly using Lambda using Zappa.
## Endpoints
### '/'
This is the default endpoint, returns 'ok' and takes no input.
### '/ping'
This must be called from a Slack workspace and just replies with 'pong' to the calling user.
### '/lunch'
This must be called from a Slack workspace and replies to the channel with the results of a call to the URL specified by the `LUNCH_REQUEST_URL` environment variable.
## Deployment
### Environment Variables
`LUNCH_REQUEST_URL` is the URL called by requests to `/lunch`; expects a simple text response
`SLACK_SIGNING_SECRET` is the signing secret set by Slack
### Setup slack
Go here https://api.slack.com/apps
Create and "install" the App and copy the signing secret into the environment where the deployment should occur.
### Choose a deployment method
#### Server or container based
Setup the prerequisites in either `pip install -r requirements.txt` or using pipenv via `pipenv istall` the key environment variables via your method of choice (.env for pipenv, .profile for venv, etc.) launch using with the flask internal webserver via `flask run` or using gunicorn with the included `run_gunicorn.sh`.
#### Serverless
Setup AWS credentials and install either install requirements zappa via `pip install zappa` then run `zappa deploy dev`.  I would call it production but I don't want that kind of responsibility in my life right now.
After completing the zappa deployment, run the `zappa status` command and get the URL.  Visit that URL in a web browser or via curl to cold-start the Lambda.
### Setup Slack Slash Command
Set the Slack App up and map the desired slash command ('/lunch' for example) to the request URL for the deployed bot ('https://example.com/lunch').  You can use the `zappa status` command to get the URL.
