from wit import Wit
from flask import Flask, request
from pymessenger.bot import Bot
import requests
import os
from tvshowlisting import tvlisting

# Insert Wit access token here. Don't forget to train the Wit bot.
access_token ='F6V6GKFJVYVXMLPC36HP7L222HGZM2TF'

# Facebook App access token. Don't forge to connect app to page.
TOKEN ='EAATQSAo4L7sBAEZBu8KjwmTlQ6Q0kXpbEJTZCX90UPwdCw3EZCsKZCrxvk0SeQ7hZCVJKza2G6ip3y4DxdgW0kGO4Ori4LsyzFrUnw92YJyIlYC1omnWeGDf3pZAu79yPU43LO4zOSLpUQgZCtidQHWgA095GRYIZBEtWpI435FVcAZDZD'

# Set up bot and flask app
bot = Bot(TOKEN)
app = Flask(__name__)

# Global variables to ensure pymessenger bot waits for wit.ai to respond.
messageToSend = 'This is default. Something is not correct'
done = False


def first_entity_value(entities, entity):
    if entity not in entities:
        return None
    val = entities[entity][0]['value']
    if not val:
        return None
    return val['value'] if isinstance(val, dict) else val


def say(session_id, context, msg):
    global messageToSend
    messageToSend = str(msg)
    global done
    done = True


def merge(session_id, context, entities, msg):
    loc = first_entity_value(entities, 'channel')
    if loc:
        context['channel'] = loc
    return context


def error(session_id, context, e):
    print(str(e))


# Calls pywapi to fetch weather info in realtime
def gettvlisting(session_id, context):
    channel = context['channel']
    context['tvshow'] = tvlisting(channel)
    return context

actions = {
    'say': say,
    'merge': merge,
    'error': error,
    'gettvlisting': gettvlisting,
}

client = Wit(access_token, actions)

# Set up webserver and respond to messages


@app.route("/webhook", methods=['GET', 'POST'])
def hello():
    # Get request according to Facebook Requirements
    if request.method == 'GET':
        if (request.args.get("hub.verify_token") == "goklunkers"):
            return request.args.get("hub.challenge")
    # Post Method for replying to messages
    if request.method == 'POST':
        output = request.json
        event = output['entry'][0]['messaging']
        for x in event:
            if (x.get('message') and x['message'].get('text')):
                message = x['message']['text']
                recipient_id = x['sender']['id']
                client.run_actions(recipient_id, message, {})
                if done:
                    print messageToSend
                    bot.send_text_message(recipient_id, messageToSend)
            else:
                pass
        return "success"

# Default test route for server
@app.route("/")
def new():
    return "Server is Online."


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port)
