import logging
import os
import re
from dotenv import load_dotenv
from telegram import Update
from playsound import playsound
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from eleven_labs import text_to_speech_file_eleven_labs, voices
from obs import set_text, set_image_enabled

DEFAULT_VOICE = 'ramzan'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

load_dotenv()


def parse_text(text):
    pattern = r"\[([\w-]+)\]\s*([^[]+)"
    matches = re.findall(pattern, text)

    result = []

    for key, value in matches:
        result.append([key, value.strip()])
    return [[key, value.strip()] for key, value in matches]


def play_text(text: str, voice: str):
    file = text_to_speech_file_eleven_labs(text, voice)
    image = voices[voice]['image']
    set_image_enabled(image, True)
    set_text(text)

    playsound(file)
    os.remove(file)

    set_image_enabled(image, False)
    set_text('')


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text

    messages = parse_text(message)
    if not messages:
        return

    print('messages: ', messages)

    for voice, text in messages:
        play_text(text, voice)

    await context.bot.send_message(chat_id=update.effective_chat.id, text=repr(messages))

if __name__ == '__main__':
    application = ApplicationBuilder().token(os.getenv('TELEGRAM_TOKEN')).build()

    echo_handler = MessageHandler(filters.TEXT, echo)
    application.add_handler(echo_handler)

    application.run_polling()
