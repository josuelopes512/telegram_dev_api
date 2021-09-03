from flask import Flask
from flask import request
import telegram, json, logging, os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

bot = telegram.Bot(token=os.environ.get("TOKEN"))

bot.sendMessage(chat_id=515489999, text='message')

if __name__ == '__main__':
    app.run(debug=True)