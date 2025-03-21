import telebot

bot = telebot.TeleBot("7556909227:AAGBffoAVMnnwRm34VLAN68IWqhhpFO1TTQ")

# Respond to the /start or /help commands
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hello! How can I assist you today?")

# Echo any other messages
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

# Start the bot
bot.polling()
