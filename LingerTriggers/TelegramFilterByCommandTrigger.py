"""
TelegramFilterByCommandTrigger listen to trigger commands from a telgram bot chat
"""

# Operation specific imports
import ast
from collections import defaultdict
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, ConversationHandler, Filters

import LingerTriggers.LingerBaseTrigger as lingerTriggers

CHOOSING = 1

class TelegramFilterByCommandTrigger(lingerTriggers.LingerBaseTrigger):
    """Trigger that engaged when a new mail is recieved thread"""

    DEFAULT_END_PHRASE = "Done"
    def __init__(self, configuration):
        super(TelegramFilterByCommandTrigger, self).__init__(configuration)
        self.actions_by_labels = defaultdict(list)

        # Fields
        self.telegram_bot_adapter_uuid = configuration["telegram_bot_adapter"]
        self.command_word = configuration["command_word"]

        # TODO this should be already a list in the configuration system
        self.authorized_users = ast.literal_eval(configuration["authorized_users"])

        self.commands = []

        self.markup = ReplyKeyboardMarkup(self.commands, one_time_keyboard=True)

        # The conversation structure
        self.conversation_handler = ConversationHandler(
            entry_points=[CommandHandler(self.command_word, self.start_command)],
            states={
                CHOOSING: [MessageHandler(Filters.text, self.trigger_check_condition)],
            },
            fallbacks=[]
        )

        # Optional fields


        self.logger.debug("TelegramFilterByCommandTrigger initialized")

    def telegram_bot_adapter(self):
        """Getter for the bot adapter"""
        return self.get_adapter_by_uuid(self.telegram_bot_adapter_uuid)

    def start_command(self, bot, update): # Telegram Handler method, can't change signature pylint: disable=w0613
        """Starting the commands listen loop"""
        if str(update.message.from_user.id) in self.authorized_users:
            update.message.reply_text(
                "Hi, ready for commands.",
                reply_markup=self.markup)

            return CHOOSING

        else:
            update.message.reply_text("Nice to meet you.")
            return ConversationHandler.END

    def trigger_check_condition(self, bot, update): # Telegram Handler method, can't change signature pylint: disable=w0613
        """Checking trigger if should enagage an action"""
        # Check authorization
        if str(update.message.from_user.id) in self.authorized_users:
            command = update.message.text
            if command == self.DEFAULT_END_PHRASE:
                update.message.reply_text("Good bye")
                return ConversationHandler.END

            elif command in self.actions_by_labels.keys():
                update.message.reply_text(
                    "Executing command: {}".format(command),
                    reply_markup=self.markup)

                self.trigger_engaged(command)

            return CHOOSING

        else:
            return ConversationHandler.END


    def trigger_engaged(self, command=None):
        trigger_data = {}
        for action in self.actions_by_labels[command]:
            self.trigger_specific_action_callback(self.uuid, action.uuid, trigger_data)

    def start(self):
        keyboard_layout = []
        self.commands.sort()
        for command in self.commands:
            keyboard_layout += [[command]]

        keyboard_layout += [[self.DEFAULT_END_PHRASE]]

        self.logger.debug(keyboard_layout)

        self.markup = ReplyKeyboardMarkup(keyboard_layout, one_time_keyboard=True)
        self.telegram_bot_adapter().add_handler(self.conversation_handler)

    def stop(self):
        self.telegram_bot_adapter().remove_handler(self.conversation_handler)

    def register_action(self, action):
        super(TelegramFilterByCommandTrigger, self).register_action(action)
        self.actions_by_labels[action.label] += [action]
        self.commands += [action.label]

class TelegramFilterByCommandTriggerFactory(lingerTriggers.LingerBaseTriggerFactory):
    """TelegramFilterByCommandTriggerFactory generates TelegramFilterByCommandTrigger instances"""
    def __init__(self):
        super(TelegramFilterByCommandTriggerFactory, self).__init__()
        self.item = TelegramFilterByCommandTrigger

    @staticmethod
    def get_instance_name():
        """Returns instance name"""
        return "TelegramFilterByCommandTrigger"

    def get_fields(self):
        fields, optional_fields = super(TelegramFilterByCommandTriggerFactory, self).get_fields()

        fields += [('telegram_bot_adapter', 'uuid'),
                   ('command_word', 'string'),
                   ('authorized_users', ('array', 'string'))]

        return (fields, optional_fields)
