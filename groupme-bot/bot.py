import requests
import time
import json
import os
from dotenv import load_dotenv
from datetime import date
from polygon.exceptions import BadResponse
import yfinance as yf

from polygon import RESTClient

load_dotenv()

BOT_ID = os.getenv("BOT_ID")
GROUP_ID = os.getenv("GROUP_ID")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
SENDER_ID = os.getenv("SENDER_ID")
LAST_MESSAGE_ID = None
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")

def send_message(text, attachments=None):
    """Send a message to the group using the bot."""
    post_url = "https://api.groupme.com/v3/bots/post"
    data = {"bot_id": BOT_ID, "text": text, "attachments": attachments or []}
    response = requests.post(post_url, json=data)
    return response.status_code == 202

def extract_stock_symbol(text):
    keyword = "stock price"
    if keyword in text:
        stock_symbol_start = text.find(keyword) + len(keyword)
        stock_symbol = text[stock_symbol_start:].strip().upper()
        return stock_symbol
    return None

def get_stock_price(stock_symbol):
    try:
        ticker = yf.Ticker(stock_symbol)
        history = ticker.history(period='1d')
        latest_close_price = history['Close'].iloc[-1]
        return f'Ticker: {stock_symbol}\nLatest Close Price: {latest_close_price}'
    except Exception as e:
        return f"Error fetching stock information for {stock_symbol}: {e}"

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

        if "stock price" in text and message["sender_type"] != "bot":
            stock_symbol = extract_stock_symbol(text)
            if stock_symbol:
                stock_info = get_stock_price(stock_symbol)
                send_message(stock_info)

        if "like this message" in text and message["sender_type"] != "bot":
            like_message(message["id"])

    LAST_MESSAGE_ID = message["id"]


def main():
    global LAST_MESSAGE_ID

    # this is an infinite loop that will try to read (potentially) new messages every 10 seconds, but you can change this to run only once or whatever you want

    while True:
        messages = get_group_messages(LAST_MESSAGE_ID)
        for message in reversed(messages):
            process_message(message)
            LAST_MESSAGE_ID = message["id"]
        time.sleep(10)

    
if __name__ == "__main__":
    main()
