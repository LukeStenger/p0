# GroupMe Bot Documentation

## Features

### 1. Greeting Testing GitHub
- Responds to "hello bot" with the word "sup." The bot only responds to Luke Stenger saying hello.

### 2. Waking Up and Dozing Off
- Greets users with "Good morning" or "Good night", if the user sends the same phrase first, it will send the identical response + the user's name afterwards.

### 3. Like Message
- Allows the bot to cause the user to like their own message by typing "like this message."

## How to Run the Bot

1. **Prerequisites**
   - Python 3.x installed.
   - Acquire required packages via: `pip install requests python-dotenv`

2. **Configuration**
   - Create a GroupMe bot and get its `BOT_ID`.
   - Get the `GROUP_ID` of the target GroupMe group.
   - Generate a GroupMe access token and set it as `ACCESS_TOKEN`.
   - Set `SENDER_ID` to be your own SENDER_ID on GroupMe.

3. **Environment Variables**
   - Create a `.env` file in the project directory.
   - Add the following variables to the `.env` file:
     ```
     BOT_ID=your_bot_id
     GROUP_ID=your_group_id
     ACCESS_TOKEN=your_access_token
     SENDER_ID=your_sender_id
     ```

4. **Run the Bot**
   - Execute the bot script using: `python3 bot.py`

5. **Interacting with the Bot**
   - Once running, the bot will respond to the commands mentioned previously (see Features).
   - Test it yourself messages like "hello bot," "good morning," "good night," or "like this message."

## Customization

- You can extend the bot by adding new features or modifying the `process_message` function in the script.

## Troubleshooting

- If the bot encounters issues, check the console for error messages and ensure the correct setup of environment variables.

---
