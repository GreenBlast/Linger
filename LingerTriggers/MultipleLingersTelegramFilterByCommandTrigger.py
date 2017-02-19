"""
MultipleLingersTelegramFilterByCommandTrigger telgram bot chat handlers to control multiple Lingers
"""

# Operation specific imports
import ast
import json
from collections import defaultdict
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, ConversationHandler, Filters

import LingerTriggers.LingerBaseTrigger as lingerTriggers

CHOOSING_LINGER = 1
CHOOSING_COMMANDS = 2

class MultipleLingersTelegramFilterByCommandTrigger(lingerTriggers.LingerBaseTrigger):
    """Trigger that engaged when a new mail is recieved thread"""

    DEFAULT_END_PHRASE = "Done"
    def __init__(self, configuration):
        super(MultipleLingersTelegramFilterByCommandTrigger, self).__init__(configuration)
        self.actions_by_labels = defaultdict(list)

        # Fields
        self.telegram_bot_adapter_uuid = configuration["telegram_bot_adapter"]
        self.command_word = configuration["command_word"]

        # TODO this should be already a list in the configuration system
        self.authorized_users = ast.literal_eval(configuration["authorized_users"])

        self.commands = []
        self.commands_list = []
        self.chosen_linger = None
        self.choesn_linger_commands = []

        self.lingers_layouts = ReplyKeyboardMarkup(self.commands, one_time_keyboard=True)
        self.markup = self.lingers_layouts

        # The conversation structure
        self.conversation_handler = ConversationHandler(
            entry_points=[CommandHandler(self.command_word, self.start_command)],
            states={
                CHOOSING_LINGER: [MessageHandler(Filters.text, self.trigger_choose_linger)],
                CHOOSING_COMMANDS: [MessageHandler(Filters.text, self.trigger_get_command)],
            },
            fallbacks=[]
        )

        # Optional fields


        self.logger.debug("MultipleLingersTelegramFilterByCommandTrigger initialized")

    def telegram_bot_adapter(self):
        """Getter for the bot adapter"""
        return self.get_adapter_by_uuid(self.telegram_bot_adapter_uuid)

    def start_command(self, bot, update): # Telegram Handler method, can't change signature pylint: disable=w0613
        """Starting the commands listen loop"""
        if str(update.message.from_user.id) in self.authorized_users:
            update.message.reply_text(
                "Hi, Choose Linger to command.",
                reply_markup=self.markup)

            return CHOOSING_LINGER

        else:
            update.message.reply_text("Nice to meet you.")
            return ConversationHandler.END


    def trigger_choose_linger(self, bot, update): # Telegram Handler method, can't change signature pylint: disable=w0613
        """Checking trigger if should enagage an action"""
        # Check authorization
        if str(update.message.from_user.id) in self.authorized_users:
            self.chosen_linger = update.message.text
            if self.chosen_linger == self.DEFAULT_END_PHRASE:
                self.chosen_linger = None
                update.message.reply_text("Good bye")
                return ConversationHandler.END

            elif self.chosen_linger in self.actions_by_labels.keys():
                update.message.reply_text(
                    "Loading commands from linger: {}".format(self.chosen_linger))

                recieved_commands = self.trigger_engaged()
                if not recieved_commands:
                    update.message.reply_text(
                    "No answer from Linger: {}".format(self.chosen_linger), reply_markup=self.markup)
                    return CHOOSING_LINGER

                self.logger.debug("got commands %s", recieved_commands)

                keyboard_layout = []
                recieved_commands.sort()
                for command in recieved_commands:
                    keyboard_layout += [[command]]
                    self.choesn_linger_commands.append(command)

                keyboard_layout += [[self.DEFAULT_END_PHRASE]]
                self.commands_list = ReplyKeyboardMarkup(keyboard_layout, one_time_keyboard=True)
                # self.commands_list = ReplyKeyboardMarkup(json.loads(received_commands), one_time_keyboard=True)
                self.markup = self.commands_list

                update.message.reply_text(
                    "Commands loaded from Linger: {}".format(self.chosen_linger),
                    reply_markup=self.markup)


            return CHOOSING_COMMANDS

        else:
            return ConversationHandler.END


    def trigger_get_command(self, bot, update): # Telegram Handler method, can't change signature pylint: disable=w0613
        """Checking trigger if should enagage an action"""
        # Check authorization

        if str(update.message.from_user.id) in self.authorized_users:
            command = update.message.text
            if command == self.DEFAULT_END_PHRASE:
                self.chosen_linger = None
                self.markup = self.lingers_layouts
                update.message.reply_text("Choose Linger to command.", reply_markup=self.markup)
                return CHOOSING_LINGER

            elif command in self.choesn_linger_commands:
                update.message.reply_text(
                    "Executing command: {}".format(command))

                self.trigger_engaged(command)

                update.message.reply_text(
                    "Command: {} finished executing, ready for commands.".format(command),
                    reply_markup=self.markup)
            else:
                update.message.reply_text(
                    "Unknown command: {}".format(self.chosen_linger),
                    reply_markup=self.markup)

            return CHOOSING_COMMANDS

        else:
            return ConversationHandler.END


    def trigger_engaged(self, command=None):
        received_commands_list = []
        trigger_data = {}
        if command:
            trigger_data["command"] = command
        else:
            trigger_data["should_return"] = True
            trigger_data["trigger_label"] = self.label
        for action in self.actions_by_labels[self.chosen_linger]:
            result = self.trigger_specific_action_callback(self.uuid, action.uuid, trigger_data)
            if result:
                received_commands_list += json.loads(result)

        return received_commands_list

    def start(self):
        keyboard_layout = []
        self.commands.sort()
        for command in self.commands:
            keyboard_layout += [[command]]

        keyboard_layout += [[self.DEFAULT_END_PHRASE]]

        self.logger.debug(keyboard_layout)

        self.lingers_layouts = ReplyKeyboardMarkup(keyboard_layout, one_time_keyboard=True)
        self.markup = self.lingers_layouts
        self.telegram_bot_adapter().add_handler(self.conversation_handler)

    def stop(self):
        self.telegram_bot_adapter().remove_handler(self.conversation_handler)

    def register_action(self, action):
        super(MultipleLingersTelegramFilterByCommandTrigger, self).register_action(action)
        self.actions_by_labels[action.label] += [action]
        self.commands += [action.label]

class TelegramFilterByCommandTriggerFactory(lingerTriggers.LingerBaseTriggerFactory):
    """TelegramFilterByCommandTriggerFactory generates MultipleLingersTelegramFilterByCommandTrigger instances"""
    def __init__(self):
        super(TelegramFilterByCommandTriggerFactory, self).__init__()
        self.item = MultipleLingersTelegramFilterByCommandTrigger

    @staticmethod
    def get_instance_name():
        """Returns instance name"""
        return "MultipleLingersTelegramFilterByCommandTrigger"

    def get_fields(self):
        fields, optional_fields = super(TelegramFilterByCommandTriggerFactory, self).get_fields()

        fields += [('telegram_bot_adapter', 'uuid'),
                   ('command_word', 'string'),
                   ('authorized_users', ('array', 'string'))]

        return (fields, optional_fields)
