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
            self.collect_commands_from_lingers()
            available_lingers = [linger_name for linger_name in self.lingers_commands_lists.keys() if self.lingers_commands_lists[linger_name]]
            update.message.reply_text("Done loading commands, \n\
            Active lingers available are: {}".format(",".join(available_lingers)), reply_markup=self.markup)
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
                # Unsetting the current chosen linger
                self.chosen_linger = None
                update.message.reply_text("No commands were loaded from Linger: {}".format(linger_name), reply_markup=self.markup)

        return CHOOSING_LINGER


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
        if command:
            trigger_data["command"] = command
        for action in self.actions_by_labels[self.chosen_linger]:
            result = self.trigger_specific_action_callback(self.uuid, action.uuid, trigger_data)

        return result

    def load_commands_from_specific_linger(self, linger_name):
        """
        Loading command from a given linger
        :param linger_name: Given linger name
        """
        received_commands_list = []
        trigger_data = {"should_return": True, "trigger_label": self.label}
        for action in self.actions_by_labels[linger_name]:
            result = self.trigger_specific_action_callback(self.uuid, action.uuid, trigger_data)
            if result:
                try:
                    received_commands_list += json.loads(result)
                except ValueError:
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

            self.lingers_commands_lists[linger_name] = {"Markup": ReplyKeyboardMarkup(keyboard_layout, one_time_keyboard=True),
            "Commands": commands}

        else:
            self.lingers_commands_lists[linger_name] = None

    def collect_commands_from_lingers(self):
        """Collecting commands from all the lingers"""

        for linger_name in self.lingers_names:
            # Check that we are still running
            with self.lock:
                if not self.running:
                    return

            self.logger.debug("Loading commands for linger %s", linger_name)
            self.load_commands_from_specific_linger(linger_name)

    def start_collect_commands(self):
        """First time call to collection of commands from linger"""
        self.collect_commands_from_lingers()
        with self.lock:
            if not self.running:
                return

        self.scheduled_job = self.scheduler.add_job(self.collect_commands_from_lingers, 'interval', seconds=self.DEFAULT_REFRESH_INTERVAL)

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

        self.running = True

        with self.lock:
            if not self.running:
                return

        self.scheduled_job = self.scheduler.add_job(self.start_collect_commands, 'date',
                                                    run_date=datetime.now() + timedelta(0, 5))

    def stop(self):
        with self.lock:
            self.running = False
            if self.scheduled_job:
                self.scheduled_job.remove()
                self.scheduled_job = None

        self.telegram_bot_adapter().remove_handler(self.conversation_handler)

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
