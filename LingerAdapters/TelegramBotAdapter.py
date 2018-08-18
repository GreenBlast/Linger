"""
TelegramBotAdapter is an adapter which implements the logic of a telegram bot
"""
import ast
import LingerAdapters.LingerBaseAdapter as lingerAdapters

# Operation specific imports
import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from io import BytesIO
import base64
import LingerConstants


class TelegramBotAdapter(lingerAdapters.LingerBaseAdapter):
    """TelegramBotAdapter using a telegram bot"""

    AUTHORIZED_USERS_DEFAULT = "[]"


    def __init__(self, configuration):
        super(TelegramBotAdapter, self).__init__(configuration)
        self.logger.debug("TelegramBotAdapter started")

        # fields
        self.auth_token = self.configuration["auth_token"]

        # Optional fields
        self.authorized_users = ast.literal_eval(configuration.get("authorized_users", self.AUTHORIZED_USERS_DEFAULT))

        self.updater = Updater(token=self.auth_token)
        self.dispatcher = self.updater.dispatcher
        self.dispatcher.add_handler(CommandHandler('user_id', self.get_user_id))
        self.dispatcher.add_error_handler(self.error)

        self.updater.start_polling()

        self.logger.info("TelegramBotAdapter configured")


    # def register_for_notifications(self):
    #     self.registered_chats = []

    # def send_message(self, subject, text):

    def get_user_id(self, bot, update): # Telegram Handler method, can't change signature pylint: disable=w0613,R0201
        """
        Replying user id
        """
        update.message.reply_text("Your id is: {}".format(update.message.from_user.id))

    def error(self, bot, update, error): # Telegram Handler method, can't change signature pylint: disable=w0613,R0201
        """
        Error handler method
        """
        self.logger.warning('Update "%s" caused error "%s"', update, error)

    def add_handler(self, handler):
        """
        Adding handler to the dispatcher
        """
        self.dispatcher.add_handler(handler)

    def remove_handler(self, handler):
        """
        Removing handler from the dispatchers
        """
        self.dispatcher.remove_handler(handler)

    def send_telegram_message(self, chat_id, subject, text, **kwargs):
        """
        Sending a message to the subscribers
        """
        if LingerConstants.IMAGE_DATA in kwargs:
            message = "{subject}\n{text}".format(subject=subject, text=text)
            bio = BytesIO()
            bio.name = 'image.jpeg'
            image_data = kwargs[LingerConstants.IMAGE_DATA]
            if isinstance(image_data, str):
                image_data = image_data.encode('utf-8')
            bio.write(image_data)
            bio.seek(0)
            self.updater.bot.send_photo(chat_id=chat_id, text=message, photo=bio)
        elif LingerConstants.IMAGE_BASE64_DATA in kwargs:
            message = "{subject}\n{text}".format(subject=subject, text=text)
            bio = BytesIO()
            bio.name = 'image.jpeg'
            image_data = base64.b64decode(kwargs[LingerConstants.IMAGE_BASE64_DATA])
            if isinstance(image_data, str):
                image_data = image_data.encode('utf-8')
            bio.write(image_data)
            bio.seek(0)
            self.updater.bot.send_photo(chat_id=chat_id, text=message, photo=bio)
        elif LingerConstants.TEXT_DATA in kwargs:
            message = kwargs[LingerConstants.TEXT_DATA]
            self.updater.bot.send_message(chat_id=chat_id, text=message)
        else:
            # Formatting message
            message = "<b>{subject}</b>\n{text}".format(subject=subject, text=text)
            self.updater.bot.send_message(chat_id=chat_id, text=message, parse_mode=telegram.ParseMode.HTML)

    def cleanup(self):
        if self.updater.running:
            self.updater.stop()


class TelegramBotAdapterFactory(lingerAdapters.LingerBaseAdapterFactory):
    """TelegramBotAdapterFactory generates TelegramBotAdapter instances"""
    def __init__(self):
        super(TelegramBotAdapterFactory, self).__init__()
        self.item = TelegramBotAdapter

    @staticmethod
    def get_instance_name():
        """Returns instance name"""
        return "TelegramBotAdapter"

    def get_fields(self):
        fields, optional_fields = super(TelegramBotAdapterFactory, self).get_fields()

        fields += [('auth_token', "string")]

        optional_fields += [('authorized_users', ('array', 'string'))]

        return fields, optional_fields
