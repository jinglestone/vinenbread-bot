import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext

# Load environment variables
load_dotenv()

API_KEY = os.getenv('API_KEY')
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')

# States for the conversation
TIME, PEOPLE, PREORDER = range(3)

# Start command handler
def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    update.message.reply_text(
        "Добро пожаловать в ресторан Vinenbread!\n\n"
        "Пожалуйста, сообщите время вашего бронирования."
    )
    return TIME

# Collect time of reservation
def time_handler(update: Update, context: CallbackContext):
    context.user_data['time'] = update.message.text
    update.message.reply_text(
        "Сколько человек будет на вашем бронировании?"
    )
    return PEOPLE

# Collect number of people
def people_handler(update: Update, context: CallbackContext):
    context.user_data['people'] = update.message.text
    update.message.reply_text(
        "Вы хотите заранее заказать еду? Если да, пожалуйста, выберите из нашего меню.\n\n"
        "Меню доступно здесь: [ссылка на меню].\n\n"
        "Пожалуйста, ответьте да или нет."
    )
    return PREORDER

# Collect pre-order information
def preorder_handler(update: Update, context: CallbackContext):
    context.user_data['preorder'] = update.message.text.lower()
    # Send the collected information to the admin
    message = (
        f"Новый запрос на бронирование!\n\n"
        f"Время бронирования: {context.user_data['time']}\n"
        f"Число людей: {context.user_data['people']}\n"
        f"Предзаказ еды: {'Да' if context.user_data['preorder'] == 'да' else 'Нет'}"
    )
    context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=message)
    
    # Send confirmation message to the user
    update.message.reply_text(
        "Спасибо за ваш запрос! Мы свяжемся с вами для подтверждения в течение 15 минут."
    )

    return ConversationHandler.END

# Cancel conversation
def cancel(update: Update, context: CallbackContext):
    update.message.reply_text("Процесс бронирования отменен. Если хотите, начните заново с /start.")
    return ConversationHandler.END

# Set up conversation handler
conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        TIME: [MessageHandler(Filters.text & ~Filters.command, time_handler)],
        PEOPLE: [MessageHandler(Filters.text & ~Filters.command, people_handler)],
        PREORDER: [MessageHandler(Filters.text & ~Filters.command, preorder_handler)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)

def main():
    # Initialize the updater and dispatcher
    updater = Updater(API_KEY, use_context=True)
    dispatcher = updater.dispatcher

    # Add conversation handler to the dispatcher
    dispatcher.add_handler(conversation_handler)

    # Start polling for updates
    updater.start_polling()

    # Run the bot until the script is terminated
    updater.idle()

if __name__ == '__main__':
    main()
