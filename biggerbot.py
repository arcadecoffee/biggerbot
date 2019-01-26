import hashlib
import hmac
import os
import requests
import time

from flask import abort, Flask, jsonify, request


app = Flask(__name__)


def is_request_valid(request):
    slack_signing_secret = os.environ['SLACK_SIGNING_SECRET']
    timestamp = request.headers['X-Slack-Request-Timestamp']
    slack_signature = request.headers['X-Slack-Signature']

    # Check the age of the request and reject if more that 5 minutes old
    if abs(time.time() - int(timestamp)) > 60 * 5:
        return

    # This is the recipe described here:
    # https://api.slack.com/docs/verifying-requests-from-slack
    sig_basestring = 'v0:' + timestamp + ':' + request.get_data(as_text=True)
    my_signature = 'v0=' + hmac.new(slack_signing_secret.encode('utf-8'),
            msg=sig_basestring.encode('utf-8'), digestmod='sha256').hexdigest()
    return hmac.compare_digest(my_signature, slack_signature)


@app.route('/', methods=['GET', 'POST'])
def default():
    return 'ok'


@app.route('/ping', methods=['POST'])
def ping():
    if not is_request_valid(request):
        abort(400)

    return jsonify(
            response_type='ephemeral',
            text='pong',
            )


@app.route('/lunch', methods=['POST'])
def lunch():
    if not is_request_valid(request):
        abort(400)

    url = os.environ['LUNCH_REQUEST_URL'] + '?day=' + \
        request.values.get('text', '')
    lunch_txt = requests.get(url).text
    if lunch_txt == '':
        lunch_txt = 'Got nothin\''
    
    return jsonify(
            response_type='in_channel',
            text='```' + lunch_txt + '```',
            )
