import subprocess
import openai
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

Token: Final = '6522414111:AAFMWw2lS-3hs80eh0EybYfgHMsJa3fD2eg'
BOT_USERNAME: Final = '@School-Managerbot'

# Setze deinen OpenAI API-Schlüssel hier ein
openai.api_key = 'DEIN_API_SCHLUESSEL'

# Lade das Deutsche Sprachmodell
# Hier solltest du den Code für das Laden des spaCy-Modells hinzufügen, wenn es benötigt wird

# Funktion zur Verarbeitung der Nachricht mit spaCy
def process_message(text):
    # Hier könntest du Logik hinzufügen, um relevante Informationen aus der Nachricht zu extrahieren
    # Hier sollte der Code für die Verarbeitung mit spaCy eingefügt werden
    pass

# Funktion zum Generieren einer GPT-3-Antwort
def generate_gpt3_response(question):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=question,
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Telegram-Bot-Funktionen
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello!, Thanks for chatting with me')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('I am a School-Manager bot, I help you to manage your School things')

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This is a custom command')

def handle_response(text: str, entities: list) -> str:
    # Hier könnte die Logik für die Verarbeitung der Entitäten eingefügt werden
    pass

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            entities = process_message(new_text)
            response = generate_gpt3_response(new_text)
        else:
            return
    else:
        entities = process_message(text)
        response = generate_gpt3_response(text)

    print('Bot:', response)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(Token).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    # Polls the bot
    print('Polling...')
    app.run_polling(poll_interval=3)
