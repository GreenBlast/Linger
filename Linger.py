import os
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

import sys
import time
import logging
import json
from datetime import datetime, timedelta
from collections import defaultdict
import uuid
from apscheduler.schedulers.background import BackgroundScheduler

LINGER_CONFIGURATION_FILEPATH = "Linger.config"

LOG_FILE_LOCATION = r"." + os.sep + r"Logs" + os.sep + time.strftime('%Y-%m-%d-%H-%M-%S') + ".log"
# LOG_LEVEL = logging.INFO
LOG_LEVEL = logging.DEBUG
logging.basicConfig(level=LOG_LEVEL,
                    format='%(asctime)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger('Linger')

formatter = logging.Formatter('%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Multiplexing log lines
file_handler = logging.FileHandler(LOG_FILE_LOCATION, mode='w')
file_handler.setFormatter(formatter)
file_handler.setLevel(LOG_LEVEL)
console = logging.StreamHandler()
console.setFormatter(formatter)
console.setLevel(LOG_LEVEL)
logger.addHandler(file_handler)

from LingerManagers.AdaptersManager import AdaptersManager
from LingerManagers.ActionsManager import ActionsManager
from LingerManagers.TriggersManager import TriggersManager

class Linger(object):
    """Linger monitors file changes, and acting according to a preset"""
    
    def __init__(self, configuration_from_file):
        self.logger = logger
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
            if(item["type"] == "Triggers"):
                self.triggers_manager.create_trigger(item)
            elif(item["type"] == "Actions"):
                self.actions_manager.create_action(item)
            elif(item["type"] == "Adapters"):
                self.adapters_manager.create_adapter(item)

        # Register triggers
        for trigger_id, trigger_action_item in self.configuration["TriggerActions"].iteritems():
            for action_id in trigger_action_item['actions']:
                self.actions_by_trigger[trigger_id][action_id] = self.actions_manager.get_action(action_id)
                self.triggers_manager.register_action_to_trigger(trigger_id, self.actions_by_trigger[trigger_id][action_id])
            
    def build_configuration(self, configuration_from_file):
        configuration = defaultdict(None)
        configuration['shutdown'] = self.shutdown
        configuration['set_should_restart'] = self.set_should_restart
        configuration['get_adapter_by_uuid'] = self.get_adapter_by_uuid
        configuration['scheduler'] = self.scheduler
        configuration['trigger_callback'] = self.trigger_callback
        configuration['trigger_specific_action_callback'] = self.trigger_specific_action_callback
        configuration['dir_paths'] = configuration_from_file['dir_paths']
        configuration['Items'] = configuration_from_file['Items']
        configuration["counter_keep_alive"] = configuration_from_file["counter_keep_alive"]
        configuration["TriggerActions"] = configuration_from_file["TriggerActions"]

        return configuration

    def trigger_callback(self, trigger_uuid, trigger_data):
        self.logger.debug("trigger calling back: %s" % (self.actions_by_trigger[trigger_uuid]))
        for action in self.actions_by_trigger[trigger_uuid].itervalues():
            action.act(trigger_data)

    def trigger_specific_action_callback(self, trigger_uuid, action_uuid,trigger_data):
        self.logger.debug("trigger calling back: %s" % (self.actions_by_trigger[trigger_uuid]))
        action = self.actions_by_trigger[trigger_uuid][action_uuid]
        action.act(trigger_data)

    def start(self):
        self.scheduler.start()
        self.keep_alive_job = self.scheduler.add_job(self.log_alive_task, 'interval', seconds=self.configuration['counter_keep_alive'])
        self.triggers_manager.start()

    def stop(self):
        self.triggers_manager.stop()
        self.keep_alive_job.remove()
        self.scheduler.shutdown(wait=True)

    def shutdown(self):
        # TODO can add here check for credentials if allowed to call it
        self.should_loop = False

    def set_should_restart(self, flag):
        self.should_restart = flag

    def get_adapter_by_uuid(self, uuid_of_adapter):
        adapter = None
        try:
            adapter = self.adapters_manager.get_adapter_by_uuid(uuid_of_adapter)
        except:
            adapter = None

        return adapter

    def log_alive_task(self):
        logger.info("Linger is still lingering")

    def loop(self):
        # TODO need to make the timeout configurable
        while self.should_loop:
            time.sleep(1)

    def clean(self):
        if self.should_restart:
            args = sys.argv[:]
            self.logger.debug('Re-spawning %s' % ' '.join(args))

            args.insert(0, sys.executable)
            if sys.platform == 'win32':
                args = ['"%s"' % arg for arg in args]
                
            os.execv(sys.executable, args)

def main():
    logger.info("Linger has started, be afraid, be very afraid, Press Ctrl+c to quit")

    with open(LINGER_CONFIGURATION_FILEPATH,'r') as configuration_file:
        json_configuration = configuration_file.read()
        configuration = json.loads(json_configuration)
        configuration_file.close()

    # Creating Linger with configuration
    linger = Linger(configuration)

    linger.start()

    try:
        linger.loop()
        logger.info("Linger has stopped working")
        linger.stop()
        logger.info("Quitting Linger")
    except KeyboardInterrupt:
        linger.stop()
        logger.info("Quitting Linger")
    finally:
        linger.clean()
        [logger.removeHandler(handler) for handler in logger.handlers]

if __name__ == '__main__':
    main()