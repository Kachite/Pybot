import telebot
import fuzzywuzzy
from fuzzywuzzy import process
import schedule
import time
import threading

# Replace with your actual bot token
BOT_TOKEN = "7556909227:AAGBffoAVMnnwRm34VLAN68IWqhhpFO1TTQ"

bot = telebot.TeleBot(BOT_TOKEN)

# Store user chat IDs for notifications
subscribed_users = set()

# Dictionary of Tinkoff FAQs and answers
faq = {
    "how to open a bank account": "To open a bank account with Tinkoff, you can download our app or visit our website and follow the steps provided.",
    "how to order a card": "To order a card, simply log into the Tinkoff app, go to the 'Cards' section, and follow the instructions to choose and order a card.",
    "how to make a transfer": "To make a transfer, open the Tinkoff app, go to the 'Transfers' section, select the recipient, and enter the amount you want to send.",
    "how to check balance": "You can check your balance directly in the Tinkoff app, or by logging into your account on our website.",
    "how to contact customer support": "To contact customer support, you can use the in-app chat, call us at 8-800-555-77-44, or email support@tinkoff.ru.",
    "how to change my personal information": "To change your personal information, log into the Tinkoff app, go to 'Profile', and select 'Edit Personal Info'.",
    "how to reset my password": "To reset your password, open the Tinkoff app, go to 'Settings', select 'Security', and follow the steps to reset your password.",
}

# Command to start the bot
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hello! I can answer your questions about Tinkoff services. Just ask me anything. Use /subscribe to receive updates.")
    subscribed_users.add(message.chat.id)

# Command to subscribe to notifications
@bot.message_handler(commands=['subscribe'])
def subscribe(message):
    subscribed_users.add(message.chat.id)
    bot.reply_to(message, "You have subscribed to automated updates!")

# Command to unsubscribe
@bot.message_handler(commands=['unsubscribe'])
def unsubscribe(message):
    subscribed_users.discard(message.chat.id)
    bot.reply_to(message, "You have unsubscribed from automated updates!")

# Function to match user queries with FAQs using fuzzy matching
def get_faq_answer(query):
    query_lower = query.lower()
    # Get the closest match to the user's query
    best_match, score = process.extractOne(query_lower, faq.keys())
    
    # If a close match is found (score > 70)
    if score > 50:
        return faq[best_match]
    
    return "Sorry, I couldn't find an answer to your question. Maybe you can try asking something like: 'How to contact customer support' or 'How to reset my password'."

# Function to handle user messages and respond with FAQ answers
@bot.message_handler(func=lambda message: True)
def respond_to_user(message):
    user_question = message.text
    answer = get_faq_answer(user_question)
    bot.reply_to(message, answer)

# Echo any received messages
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

# Start the bot
bot.polling()
