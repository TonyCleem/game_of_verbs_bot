import os
from dotenv import load_dotenv

import logging

from telegram import Update, ForceReply
from telegram.ext import (
    Updater,
    Filters,
    CommandHandler,
    MessageHandler,
    CallbackContext,
)

from google.cloud import dialogflow


load_dotenv()
TOKEN = os.environ["TELEGRAM_TOKEN_BOT"]
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user

    update.message.reply_markdown_v2(
        rf"Привет {user.mention_markdown_v2()}\!",
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Help!")


def handle_message(update, context):
    message = update.message.text
    session_id = str(update.effective_user.id)

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(PROJECT_ID, session_id)
    text_input = dialogflow.TextInput(text=message, language_code="ru")
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    update.message.reply_text(response.query_result.fulfillment_text)


def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, handle_message)
    )
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
