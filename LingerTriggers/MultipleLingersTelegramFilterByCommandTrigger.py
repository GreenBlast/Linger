"""
MultipleLingersTelegramFilterByCommandTrigger telgram bot chat handlers to control multiple Lingers
"""

# Operation specific imports
import ast
import json
import threading
from collections import defaultdict
from datetime import datetime, timedelta
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, ConversationHandler, Filters

import LingerConstants
import LingerTriggers.LingerBaseTrigger as lingerTriggers

CHOOSING_LINGER = 1
CHOOSING_COMMANDS = 2


class MultipleLingersTelegramFilterByCommandTrigger(lingerTriggers.LingerBaseTrigger):
    """Trigger that engaged when a new mail is recieved thread"""

    DEFAULT_END_PHRASE = "Done"
    DEFAULT_REFRESH_PHRASE = "Refresh"
    DEFAULT_REFRESH_INTERVAL = 300.0

    def __init__(self, configuration):
        super(MultipleLingersTelegramFilterByCommandTrigger, self).__init__(configuration)
        self.actions_by_labels = defaultdict(list)

        # Fields
        self.telegram_bot_adapter_uuid = configuration["telegram_bot_adapter"]
        self.command_word = configuration["command_word"]

        # TODO this should be already a list in the configuration system
        self.authorized_users = ast.literal_eval(configuration["authorized_users"])

        self.lock = threading.Lock()
        self.running = False
        self.lingers_names = []
        self.chosen_linger = None
        self.scheduled_job = None
        self.lingers_commands_lists = {}

        self.lingers_layouts = ReplyKeyboardMarkup(self.lingers_names, one_time_keyboard=True)
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

        self.logger.debug("MultipleLingersTelegramFilterByCommandTrigger initialized")

    def telegram_bot_adapter(self):
        """Getter for the bot adapter"""
        return self.get_adapter_by_uuid(self.telegram_bot_adapter_uuid)

    def start_command(self, bot, update):  # Telegram Handler method, can't change signature pylint: disable=w0613
        """Starting the commands listen loop"""
        # Check authorization
        if str(update.message.from_user.id) not in self.authorized_users:
            update.message.reply_text("Nice to meet you.")
            return ConversationHandler.END

        # Else, user it authorized
        update.message.reply_text(
            "Hi, Choose Linger to command.",
            reply_markup=self.markup)

        return CHOOSING_LINGER

    def trigger_choose_linger(self, bot, update):  # Telegram Handler method, can't change signature pylint: disable=w0613
        """Checking trigger if should enagage an action"""
        # Check authorization
        if str(update.message.from_user.id) not in self.authorized_users:
            return ConversationHandler.END

        # Else, user it authorized
        self.chosen_linger = update.message.text
        if self.chosen_linger == self.DEFAULT_END_PHRASE:
            self.chosen_linger = None
            update.message.reply_text("Good bye")
            return ConversationHandler.END

        if self.chosen_linger == self.DEFAULT_REFRESH_PHRASE:
            self.chosen_linger = None
            update.message.reply_text("Refreshing lingers...\nThis might take some time...")
            # TODO: Set not yet got from lingers, to update about command loading
            self.collect_commands_from_lingers()
            update.message.reply_text("Sent requests for commands", reply_markup=self.markup)
            return CHOOSING_LINGER

        elif self.chosen_linger in self.lingers_names:
            # TODO: Here should reply about the last time linger returned answer
            #update.message.reply_text(
            #    "Loading commands from linger: {}".format(self.chosen_linger))
            if self.lingers_commands_lists.get(self.chosen_linger, None):

                self.markup = self.lingers_commands_lists[self.chosen_linger]["Markup"]

                update.message.reply_text(
                    "Commands loaded from Linger: {}".format(self.chosen_linger),
                    reply_markup=self.markup)

                return CHOOSING_COMMANDS

            else:
                # No commands for given linger
                linger_name = self.chosen_linger
                # Un-setting the current chosen linger
                self.chosen_linger = None
                update.message.reply_text("No commands were loaded from Linger: {}".format(linger_name), reply_markup=self.markup)

        return CHOOSING_LINGER

    def trigger_get_command(self, bot, update): # Telegram Handler method, can't change signature pylint: disable=w0613
        """Checking trigger if should engage an action"""
        # Check authorization
        if str(update.message.from_user.id) in self.authorized_users:
            command = update.message.text
            if command == self.DEFAULT_END_PHRASE:
                self.chosen_linger = None
                self.markup = self.lingers_layouts
                update.message.reply_text("Choose Linger to command.", reply_markup=self.markup)
                return CHOOSING_LINGER

            elif command in self.lingers_commands_lists[self.chosen_linger]["Commands"]:
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
        trigger_data = {}
        result = None
        if command:
            trigger_data[LingerConstants.COMMAND_NAME] = command
        for action in self.actions_by_labels[self.chosen_linger]:
            result = self.trigger_specific_action_callback(self.uuid, action.uuid, trigger_data)

        return result

    def collect_commands_from_lingers(self):
        """Requesting commands from all the lingers"""

        for linger_name in self.lingers_names:
            self.logger.debug("Requesting commands for linger %s", linger_name)
            trigger_data = {LingerConstants.TRIGGER_ACTION: LingerConstants.REQUEST_COMMAND_ACTION,
                            LingerConstants.TRIGGER_CALLBACK: self.command_retrieve_callback}
            for action in self.actions_by_labels[linger_name]:
                self.trigger_specific_action_callback(self.uuid, action.uuid, trigger_data)

    def start(self):
        # Building the list of lingers to command
        keyboard_layout = []
        self.lingers_names.sort()
        for linger_name in self.lingers_names:
            keyboard_layout += [[linger_name]]

        keyboard_layout += [[self.DEFAULT_REFRESH_PHRASE]]
        keyboard_layout += [[self.DEFAULT_END_PHRASE]]

        self.logger.debug(keyboard_layout)

        self.lingers_layouts = ReplyKeyboardMarkup(keyboard_layout, one_time_keyboard=True)
        self.markup = self.lingers_layouts
        self.telegram_bot_adapter().add_handler(self.conversation_handler)

        self.subscribe_to_actions()

    def command_retrieve_callback(self, linger_name, payload, **kwargs):
        """
        Loads command retrieved from another linger, as a callback
        """
        self.logger.debug("Got payload:%s for linger:%s", payload, linger_name)
        received_commands_list = None
        if payload:
            try:
                loaded_payload = json.loads(payload.decode("utf-8"))
                received_commands_list = loaded_payload.get(LingerConstants.LABELS_LIST, None)
            except ValueError:
                self.logger.error("Not a JSON", exc_info=True)
                received_commands_list = None
            except TypeError:
                self.logger.error("Got bytes instead of string", exc_info=True)
                received_commands_list = None


        self.logger.debug("got commands %s", received_commands_list)

        if received_commands_list:
            keyboard_layout = []
            commands = []
            received_commands_list.sort()
            for command in received_commands_list:
                keyboard_layout += [[command]]
                commands.append(command)

            keyboard_layout += [[self.DEFAULT_END_PHRASE]]

            with self.lock:
                self.lingers_commands_lists[linger_name] = {"Markup": ReplyKeyboardMarkup(keyboard_layout, one_time_keyboard=True),
                "Commands": commands}

    def subscribe_to_actions(self):
        for linger_name in self.lingers_names:
            trigger_data = {LingerConstants.TRIGGER_ACTION: LingerConstants.SUBSCRIBE_ACTION,
                            LingerConstants.TRIGGER_CALLBACK: self.command_retrieve_callback,
                            LingerConstants.LINGER_NAME:linger_name}
            for action in self.actions_by_labels[linger_name]:
                self.trigger_specific_action_callback(self.uuid, action.uuid, trigger_data)

    def unsubscribe_from_actions(self):
        for linger_name in self.lingers_names:
            trigger_data = {LingerConstants.TRIGGER_ACTION: LingerConstants.UNSUBSCRIBE_ACTION,
                            LingerConstants.TRIGGER_CALLBACK: self.command_retrieve_callback}
            for action in self.actions_by_labels[linger_name]:
                self.trigger_specific_action_callback(self.uuid, action.uuid, trigger_data)

    def stop(self):
        self.telegram_bot_adapter().remove_handler(self.conversation_handler)
        self.unsubscribe_from_actions()

    def register_action(self, action):
        super(MultipleLingersTelegramFilterByCommandTrigger, self).register_action(action)
        self.actions_by_labels[action.label] += [action]
        self.lingers_names += [action.label]


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

        return fields, optional_fields
