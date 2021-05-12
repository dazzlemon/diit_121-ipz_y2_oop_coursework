from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def menu(update, _context):
    keyboard = [
        [
            InlineKeyboardButton('Whole schedule', callback_data='whole_schedule'),
            InlineKeyboardButton('Schedule for this week', callback_data='Schedule for this week'),
        ],
        [
            InlineKeyboardButton('Schedule for today', callback_data='Schedule for today'),
            InlineKeyboardButton('Schedule for tomorrow', callback_data='Schedule for tomorrow'),
        ],
        [
            InlineKeyboardButton('Current subject', callback_data='Current subject'),
            InlineKeyboardButton('Next subject', callback_data='Next subject'),
        ],
        [
            InlineKeyboardButton('more', callback_data='more'),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)


def button(update, context):
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    if query.data == 'whole_schedule':
        query.edit_message_text(text='whole schedule:')
        context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo='https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse1.mm.bing.net%2Fth%3Fid%3DOIP.z9DgCgl3z9jhbiJDMuwsOAHaEK%26pid%3DApi&f=1'
        )
    else:
        query.edit_message_text(text=f"Selected option: {query.data}")
