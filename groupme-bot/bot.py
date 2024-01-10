import requests
import time
import json
import os
from dotenv import load_dotenv

load_dotenv()

BOT_ID = os.getenv("BOT_ID")
GROUP_ID = os.getenv("GROUP_ID")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
SENDER_ID = os.getenv("SENDER_ID")
LAST_MESSAGE_ID = None

def send_message(text, attachments=None):
    """Send a message to the group using the bot."""
    post_url = "https://api.groupme.com/v3/bots/post"
    data = {"bot_id": BOT_ID, "text": text, "attachments": attachments or []}
    response = requests.post(post_url, json=data)
    return response.status_code == 202


def get_group_messages(since_id=None):
    """Retrieve recent messages from the group."""
    params = {"token": ACCESS_TOKEN}
    if since_id:
        params["since_id"] = since_id

    get_url = f"https://api.groupme.com/v3/groups/{GROUP_ID}/messages"
    response = requests.get(get_url, params=params)
    if response.status_code == 200:
        # this shows how to use the .get() method to get specifically the messages but there is more you can do (hint: sample.json)
        return response.json().get("response", {}).get("messages", [])
    return []

def like_message(message_id):
    """Like a specific message."""
    like_url = f"https://api.groupme.com/v3/messages/{GROUP_ID}/{message_id}/like?token={ACCESS_TOKEN}"
    response = requests.post(like_url)
    return response.status_code == 200


def process_message(message):
    """Process and respond to a message."""
    global LAST_MESSAGE_ID
    text = message["text"].lower()
    user = message["user_id"]
    send = message["sender_id"]
    sender_type = message["sender_type"]
    user_name = message["name"]

    if sender_type != "bot" and LAST_MESSAGE_ID is not None:

        # i.e. responding to a specific message (note that this checks if "hello bot" is anywhere in the message, not just the beginning)
        if "hello bot" in text and user == SENDER_ID:
            send_message("sup")
            

        if message["sender_type"] != "bot" and "good morning" in text:
            send_message(f"Good morning, {user_name}!")

        if message["sender_type"] != "bot" and "good night" in text:
            send_message(f"Good night, {user_name}!")

        if "like this message" in text:
            like_message(message["id"])

    LAST_MESSAGE_ID = message["id"]


def main():
    global LAST_MESSAGE_ID
    global LAST_MESSAGE_TIMESTAMP
    # this is an infinite loop that will try to read (potentially) new messages every 10 seconds, but you can change this to run only once or whatever you want

    while True:
        messages = get_group_messages(LAST_MESSAGE_ID)
        for message in reversed(messages):
            process_message(message)
        time.sleep(10)



if __name__ == "__main__":
    main()
