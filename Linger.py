"""
Linger is a system that handles configurable triggers to actions
"""
import os
import sys
import time
import logging
import json
from collections import defaultdict
from apscheduler.schedulers.background import BackgroundScheduler

from LingerManagers.AdaptersManager import AdaptersManager
from LingerManagers.ActionsManager import ActionsManager
from LingerManagers.TriggersManager import TriggersManager

ABSPATH = os.path.abspath(__file__)
DIR_NAME = os.path.dirname(ABSPATH)
os.chdir(DIR_NAME)

LINGER_CONFIGURATION_FILEPATH = "Linger.config"

LOG_FILE_LOCATION = r"." + os.sep + r"Logs" + os.sep + time.strftime('%Y-%m-%d-%H-%M-%S') + ".log"
# LOG_LEVEL = logging.INFO
LOG_LEVEL = logging.DEBUG
logging.basicConfig(level=LOG_LEVEL,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

LOGGER = logging.getLogger('Linger')

FORMATTER = logging.Formatter('%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Multiplexing log lines
FILE_HANDLER = logging.FileHandler(LOG_FILE_LOCATION, mode='w')
FILE_HANDLER.setFormatter(FORMATTER)
FILE_HANDLER.setLevel(LOG_LEVEL)
CONSOLE_HANDLER = logging.StreamHandler()
CONSOLE_HANDLER.setFormatter(FORMATTER)
CONSOLE_HANDLER.setLevel(LOG_LEVEL)
LOGGER.addHandler(FILE_HANDLER)


class Linger(object):
    """Linger monitors file changes, and acting according to a preset"""

    def __init__(self, configuration_from_file):
        self.logger = LOGGER
        self.should_loop = True
        self.should_restart = False

        job_defaults = {
            'misfire_grace_time': None,
            'coalesce': True,
            'max_instances': 1
        }

        self.scheduler = BackgroundScheduler(job_defaults=job_defaults)
        # logging.getLogger('apscheduler').setLevel(logging.WARNING)

        self.configuration = self.build_configuration(configuration_from_file)

        self.keep_alive_job = None

        # Pair trigger to it's respective action
        self.actions_by_trigger = defaultdict(dict)
        self.adapters_manager = AdaptersManager(self.configuration)
        self.actions_manager = ActionsManager(self.configuration)
        self.triggers_manager = TriggersManager(self.configuration)

        for item in self.configuration["Items"].itervalues():
            if item["type"] == "Triggers":
                self.triggers_manager.create_trigger(item)
            elif item["type"] == "Actions":
                self.actions_manager.create_action(item)
            elif item["type"] == "Adapters":
                self.adapters_manager.create_adapter(item)

        # Register triggers
        for trigger_id, trigger_action_item in self.configuration["TriggerActions"].iteritems():
            if trigger_action_item['enabled']:
                self.triggers_manager.set_enabled(trigger_id)
            for action_id in trigger_action_item['actions']:
                self.actions_by_trigger[trigger_id][action_id] = self.actions_manager.get_action(action_id)
                self.triggers_manager.register_action_to_trigger(trigger_id, self.actions_by_trigger[trigger_id][action_id])

    def build_configuration(self, configuration_from_file):
        """
        Building the configuration to be sent to the items
        """
        configuration = defaultdict(None)
        configuration['shutdown'] = self.shutdown
        configuration['set_should_restart'] = self.set_should_restart
        configuration['get_adapter_by_uuid'] = self.get_adapter_by_uuid
        configuration['get_trigger_labels_of_actions'] = self.get_trigger_labels_of_actions
        configuration['scheduler'] = self.scheduler
        configuration['trigger_callback'] = self.trigger_callback
        configuration['trigger_specific_action_callback'] = self.trigger_specific_action_callback
        configuration['dir_paths'] = configuration_from_file['dir_paths']
        configuration['Items'] = configuration_from_file['Items']
        configuration["counter_keep_alive"] = configuration_from_file["counter_keep_alive"]
        configuration["TriggerActions"] = configuration_from_file["TriggerActions"]

        return configuration

    def trigger_callback(self, trigger_uuid, trigger_data):
        """
        Activating an action according to trigger
        """
        self.logger.debug("trigger calling back: %s", self.actions_by_trigger[trigger_uuid])
        for action in self.actions_by_trigger[trigger_uuid].itervalues():
            action.act(trigger_data)

    def trigger_specific_action_callback(self, trigger_uuid, action_uuid, trigger_data): # Want this method name! pylint: disable=C0103
        """
        Activating an action according to trigger and the action label recieved by the trigger
        """
        self.logger.debug("trigger calling back: %s", self.actions_by_trigger[trigger_uuid])
        action = self.actions_by_trigger[trigger_uuid][action_uuid]
        return action.act(trigger_data)

    def start(self):
        """
        Starting Linger activity
        """
        self.scheduler.start()
        self.keep_alive_job = self.scheduler.add_job(self.log_alive_task, 'interval', seconds=self.configuration['counter_keep_alive'])
        self.adapters_manager.start()
        self.triggers_manager.start()

    def stop(self):
        """
        Stopping Linger activity
        """
        self.triggers_manager.stop()
        self.adapters_manager.stop()
        self.keep_alive_job.remove()
        self.scheduler.shutdown(wait=True)

    def shutdown(self):
        """
        Setting Linger to stop loop and shutdown
        """
        # TODO can add here check for credentials if allowed to call it
        self.should_loop = False

    def set_should_restart(self, flag):
        """
        Setting should restart flag
        """
        self.should_restart = flag

    def get_adapter_by_uuid(self, uuid_of_adapter):
        """
        Returns adapater instance by its ID
        """
        adapter = None
        try:
            adapter = self.adapters_manager.get_adapter_by_uuid(uuid_of_adapter)
        except Exception: # Don't want to crash pylint: disable=W0703
            adapter = None

        return adapter

    def get_trigger_labels_of_actions(self, uuid_of_trigger):
        """
        Returns adapater instance by its ID
        """
        trigger_actions_labels = None
        try:
            trigger_actions_labels = self.triggers_manager.get_trigger_labels_of_actions(uuid_of_trigger)
        except Exception: # Don't want to crash pylint: disable=W0703
            trigger_actions_labels = None

        return trigger_actions_labels

    @staticmethod
    def log_alive_task():
        """
        Writing keep alive to log
        """
        LOGGER.info("Linger is still lingering")

    def loop(self):
        """
        Blocking loop function to keep running the main thread
        """
        # TODO need to make the timeout and log alive task configurable
        while self.should_loop:
            time.sleep(1)

    def clean(self):
        """
        Cleaning up before shutting down
        """
        self.adapters_manager.cleanup()
        self.actions_manager.cleanup()
        self.triggers_manager.cleanup()
        if self.should_restart:
            args = sys.argv[:]
            self.logger.debug('Re-spawning %s', args)

            args.insert(0, sys.executable)
            if sys.platform == 'win32':
                args = ['"%s"' % arg for arg in args]

            os.execv(sys.executable, args)

def main():
    """
    Linger main function, loads configuration and starting
    """
    LOGGER.info("Linger has started, be afraid, be very afraid, Press Ctrl+c to quit")

    with open(LINGER_CONFIGURATION_FILEPATH, 'r') as configuration_file:
        json_configuration = configuration_file.read()
        configuration = json.loads(json_configuration)
        configuration_file.close()

    # Creating Linger with configuration
    linger = Linger(configuration)

    linger.start()

    try:
        linger.loop()
        LOGGER.info("Linger has stopped working")
        linger.stop()
        LOGGER.info("Quitting Linger")
    except KeyboardInterrupt:
        linger.stop()
        LOGGER.info("Quitting Linger")
    finally:
        linger.clean()
        # Cleaning loggers
        map(LOGGER.removeHandler, LOGGER.handlers)

if __name__ == '__main__':
    main()
