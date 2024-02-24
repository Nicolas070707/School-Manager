import subprocess
from typing import Final
from telegram.ext import filters
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, CallbackQueryHandler
from fuzzywuzzy import process

Token: Final = '6522414111:AAFMWw2lS-3hs80eh0EybYfgHMsJa3fD2eg'
BOT_USERNAME: Final = '@School-Managerbot'

FAQ = {
    'how are you': 'I am fine, thank you! And how are you?',
    'what is your name': 'My name is ChatGPT.',
    'what is the weather today': 'The weather today is sunny.',
    'goodbye': 'Goodbye! See you next time.',
    'what is your purpose': 'My purpose is to answer questions and provide assistance.',
    'how old are you': 'I am a computer program and have no age in the human sense.',
    'where are you from': 'I am a digital program and exist wherever my code is executed.',
    'who created you': 'I was created by OpenAI.',
    'what can you do': 'I can answer questions, provide assistance, and respond to various topics.',
    'tell me a joke': [
        "Why did the math book cry? Because it had too many problems.",
        "What is green and runs through the forest? A pack of cucumbers.",
        "Why does the refrigerator have light? Because it's open."
    ],
    'what is your favorite color': 'I am a computer program, I have no favorites.',
    'do you have siblings': 'As a computer program, I have no siblings.',
    'what is the meaning of life': 'The meaning of life is a philosophical question and can be interpreted differently by each person.'
}

def generate_response(question):
    best_match, score = process.extractOne(question.lower(), FAQ.keys())
    if score >= 80:
        response = FAQ[best_match]
        if isinstance(response, list):
            return random.choice(response)
        else:
            return response
    else:
        return "Sorry, I didn't understand that. Could you please clarify?"

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hallo! Danke, dass du mit mir chattest.')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Ich bin ein School-Manager Bot. Hier sind einige Fragen, die du mir stellen kannst:\n'
                                    '/commands - Liste alle verfügbaren Befehle auf\n'
                                    '/help - Zeige diese Hilfemeldung an')

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Dies ist ein benutzerdefinierter Befehl.')

async def commands_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = 'Hier sind die Fragen, die du mir stellen kannst:\n\n'
    for question in FAQ.keys():
        message += f'- {question}\n'
    await update.message.reply_text(message)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if 'webuntis' in text.lower():
        subprocess.Popen(['python', 'Code/Python-Code/p.py'])
        await update.message.reply_text('Das WebUntis-Skript wurde gestartet.')
    elif message_type == 'group' and BOT_USERNAME in text:
        new_text: str = text.replace(BOT_USERNAME, '').strip()
        response = generate_response(new_text)
        if response == "Sorry, I didn't understand that. Could you please clarify?":
            buttons = [[InlineKeyboardButton('Ja', callback_data='yes'), 
                        InlineKeyboardButton('Nein', callback_data='no')]]
            keyboard_markup = InlineKeyboardMarkup(buttons)
            await update.message.reply_text(response, reply_markup=keyboard_markup)
        else:
            await update.message.reply_text(response)
    elif message_type == 'private':
        response: str = generate_response(text)
        if response == "Sorry, I didn't understand that. Could you please clarify?":
            buttons = [[InlineKeyboardButton('Ja', callback_data='yes'), 
                        InlineKeyboardButton('Nein', callback_data='no')]]
            keyboard_markup = InlineKeyboardMarkup(buttons)
            await update.message.reply_text(response, reply_markup=keyboard_markup)
        else:
            await update.message.reply_text(response)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query.data == 'yes':
        await query.answer('Bitte formuliere deine Frage neu.')
    elif query.data == 'no':
        await query.answer('Okay, lass mich wissen, wenn du Hilfe bei etwas anderem brauchst.')

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} hat einen Fehler verursacht: {context.error}')

def main():
    print('Bot wird gestartet...')
    app = Application.builder().token(Token).build()

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))
    app.add_handler(CommandHandler('commands', commands_command))

    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    app.add_handler(CallbackQueryHandler(button))

    app.add_error_handler(error)

    print('Umfragen...')
    app.run_polling(poll_interval=3)

if __name__ == "__main__":
    main()
