import LingerAdapters.LingerBaseAdapter as lingerAdapters 

# Operation specific imports
import ast
from telegram.ext import CommandHandler

class TelegramCommunicationAdapter(lingerAdapters.LingerBaseAdapter):
    """TelegramCommunicationAdapter ables sending messages to telegram chats after subscribing"""

    def __init__(self, configuration):
        super(TelegramCommunicationAdapter, self).__init__(configuration)
        self.logger.debug("TelegramCommunicationAdapter started")

        # fields
        self.telegram_bot_adapter_uuid = configuration["telegram_bot_adapter"]
        self.subscribe_chat_command = configuration["subscribe_chat_command"]
        self.unsubscribe_chat_command = configuration["unsubscribe_chat_command"]
 
       # TODO this should be already a list in the configuration system
        self.authorized_users = ast.literal_eval(configuration["authorized_users"])


        self.chat_set = set()

        self.subscribe_handler = CommandHandler(self.subscribe_chat_command, self.subscribe)
        self.unsubscribe_handler = CommandHandler(self.unsubscribe_chat_command, self.unsubscribe)

        self.logger.info("TelegramCommunicationAdapter configured")

    def telegram_bot_adapter(self):
        return self.get_adapter_by_uuid(self.telegram_bot_adapter_uuid)

    def subscribe(self, bot, update):
        if str(update.message.from_user.id) in self.authorized_users:
            self.chat_set.add(update.message.chat_id)

    def unsubscribe(self, bot, update):
        if str(update.message.from_user.id) in self.authorized_users:
            try:
                self.chat_set.remove(update.message.chat_id)
            except KeyError as e:
                self.logger.warn("Tried to remove unsubscribed chat_id: {}".format(update.message.chat_id))

    def send_message(self, subject, text):
        for chat_id in self.chat_set:
            self.telegram_bot_adapter().send_message(chat_id, subject, text)

    def cleanup(self):
        try:
            self.telegram_bot_adapter().remove_handler(self.subscribe_handler)
            self.telegram_bot_adapter().remove_handler(self.unsubscribe_handler)
        except Exception as e:
            self.logger.debug("Error while unsubscribing")

    def start(self):
        self.telegram_bot_adapter().add_handler(self.subscribe_handler)
        self.telegram_bot_adapter().add_handler(self.unsubscribe_handler)

    def stop(self):
        self.telegram_bot_adapter().remove_handler(self.subscribe_handler)
        self.telegram_bot_adapter().remove_handler(self.unsubscribe_handler)


class TelegramCommunicationAdapterFactory(lingerAdapters.LingerBaseAdapterFactory):
    """TelegramCommunicationAdapterFactory generates TelegramCommunicationAdapter instances"""
    def __init__(self):
        super(TelegramCommunicationAdapterFactory, self).__init__()
        self.item = TelegramCommunicationAdapter 
    
    def get_instance_name(self):
        return "TelegramCommunicationAdapter"

    def get_fields(self):
        fields, optional_fields = super(TelegramCommunicationAdapterFactory, self).get_fields()

        fields += [('telegram_bot_adapter','uuid'),
                    ('subscribe_chat_command', 'string'),
                    ('unsubscribe_chat_command', 'string'),
                    ('authorized_users', ('array', 'string'))]

        return (fields,optional_fields)
