import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, ConversationHandler, CallbackContext, Application
from telegram.ext.filters import Text

# Load environment variables
load_dotenv()

API_KEY = os.getenv('API_KEY')
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')

# States for the conversation
NAME, PHONE, TIME, PEOPLE, PREORDER = range(5)

# Start command handler
async def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    await update.message.reply_text(
        "Добро пожаловать в ресторан \"Вино и Хлеб\"!\n\n"
        "Для бронирования столика, пожалуйста, представьтесь."
    )
    return NAME

# Collect name
async def name_handler(update: Update, context: CallbackContext):
    context.user_data['name'] = update.message.text
    await update.message.reply_text(
        "Спасибо! Пожалуйста, оставьте номер телефона для связи с вами."
    )
    return PHONE

# Collect phone
async def phone_handler(update: Update, context: CallbackContext):
    context.user_data['phone'] = update.message.text
    await update.message.reply_text(
        "На какое время вы хотели бы забронировать столик?"
    )
    return TIME

# Collect time of reservation
async def time_handler(update: Update, context: CallbackContext):
    context.user_data['time'] = update.message.text
    await update.message.reply_text(
        "Сколько человек будет на вашем бронировании?"
    )
    return PEOPLE

# Collect number of people
async def people_handler(update: Update, context: CallbackContext):
    context.user_data['people'] = update.message.text
    await update.message.reply_text(
        "Вы хотите заранее заказать еду? Если да, пожалуйста, выберите из нашего меню.\n\n"
        "Меню доступно в нашем Instagram: https://www.instagram.com/vino.hleb/\n\n"
        "Пожалуйста, ответьте да или нет."
    )
    return PREORDER

# Collect pre-order information
async def preorder_handler(update: Update, context: CallbackContext):
    context.user_data['preorder'] = update.message.text.lower()
    # Send the collected information to the admin
    message = (
        f"Новый запрос на бронирование!\n\n"
        f"Имя клиента: {context.user_data['name']}\n"
        f"Телефон: {context.user_data['phone']}\n"
        f"Время бронирования: {context.user_data['time']}\n"
        f"Число людей: {context.user_data['people']}\n"
        f"Предзаказ еды: {'Да' if context.user_data['preorder'] == 'да' else 'Нет'}"
    )
    await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=message)
    
    # Send confirmation message to the user
    await update.message.reply_text(
        f"Спасибо за ваш запрос, {context.user_data['name']}! "
        "Мы свяжемся с вами для подтверждения в течение 15 минут по указанному номеру телефона."
    )
    return ConversationHandler.END

# Cancel conversation
async def cancel(update: Update, context: CallbackContext):
    await update.message.reply_text("Процесс бронирования отменен. Если хотите, начните заново с /start.")
    return ConversationHandler.END

def main():
    # Initialize the Application
    application = Application.builder().token(API_KEY).build()

    # Set up conversation handler
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NAME: [MessageHandler(Text(), name_handler)],
            PHONE: [MessageHandler(Text(), phone_handler)],
            TIME: [MessageHandler(Text(), time_handler)],
            PEOPLE: [MessageHandler(Text(), people_handler)],
            PREORDER: [MessageHandler(Text(), preorder_handler)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    # Add conversation handler to the application
    application.add_handler(conversation_handler)

    # Start the bot
    print("Starting bot...")
    application.run_polling(stop_signals=None)

if __name__ == '__main__':
    main()