from telegram import InlineKeyboardButton, InlineKeyboardMarkup


class MenuManager:
    def __init__(self):
        self.last_kb = None
        self.current = None


    def button_handler(self, update, _context):
        query = update.callback_query

        # CallbackQueries need to be answered, even if no notification to the user is needed
        # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
        query.answer()

        if query.data == 'exit':
            query.delete_message()
        elif query.data == 'back' and self.last_kb is not None:
            query.edit_message_reply_markup(reply_markup=self.last_kb)
        elif query.data == 'day':
            self.last_kb = menu_day()
            query.edit_message_reply_markup(reply_markup=menu_day())
        elif query.data == 'week':
            pass
        elif query.data == 'subject_now':
            pass
        elif query.data == 'subject_next':
            pass
        elif query.data == 'more':
            pass
        # elif query.data == 'whole_schedule':
        #     query.edit_message_text(text='whole schedule:')
        #     context.bot.send_photo(
        #         chat_id=update.effective_chat.id,
        #         photo='https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Ftse1.mm.bing.net%2Fth%3Fid%3DOIP.z9DgCgl3z9jhbiJDMuwsOAHaEK%26pid%3DApi&f=1'
        #     )
        else:
            query.edit_message_text(text="ERROR")


    def keyboard(self):
        kb = [
            [
                InlineKeyboardButton('Day', callback_data='day'),
            ],
            [
                InlineKeyboardButton('Week', callback_data='week'),
            ],
            [
                InlineKeyboardButton('Current subject', callback_data='subject_now'),
                InlineKeyboardButton('Next subject', callback_data='subject_next'),
            ],
            [
                InlineKeyboardButton('more', callback_data='more'),
            ],
            [
                InlineKeyboardButton('Exit', callback_data='exit'),
            ],
        ]
        return InlineKeyboardMarkup(kb)


    def menu(self, update, _context):
        self.last_kb = self.current
        self.current = self.keyboard()
        update.message.reply_text('Please choose:', reply_markup=self.keyboard())


def menu_day():
    keyboard = [
        [
            InlineKeyboardButton('Today', callback_data='today'),
        ],
        [
            InlineKeyboardButton('Tomorrow', callback_data='tomorrow'),
        ],
        [
            InlineKeyboardButton('Calendar Day', callback_data='day_calendar'),
        ],
        [
            InlineKeyboardButton('Week Day', callback_data='day_week'),
        ],
        [
            InlineKeyboardButton('Back', callback_data='back'),
        ],
        [
            InlineKeyboardButton('Exit', callback_data='exit'),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)
