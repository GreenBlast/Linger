import ast

import LingerConstants
import LingerTriggers.LingerBaseTrigger as lingerTriggers

# Operation specific imports
import os
from pathtools.patterns import match_path


class WatchedPathNotADirectoryException(Exception):
    """WatchedPathNotADirectoryException is raised when the given watched path is not a directory"""
    pass        


class DirWatchTrigger(lingerTriggers.LingerBaseTrigger):
    """Trigger watches for changes in a directory"""
    PATTERNS_DEFAULT = r"""["*.*"]"""
    IGNORED_PATTERNS_DEFAULT = """[]"""
    ALLOWED_TRIGGER_TYPES_DEFAULT = "[\'modified\', \'created\', \'moved\', \'deleted\']"

    def __init__(self, configuration):
        super(DirWatchTrigger, self).__init__(configuration)

        # Fields
        self.dir_watch_adapter_uuid = self.configuration["dir_watch_adapter_uuid"]
        # Checks if really a directory
        self.watched_path = os.path.abspath(self.configuration["watched_path"])

        if os.path.isdir(self.watched_path) is not True: 
            raise WatchedPathNotADirectoryException(self.watched_path)
        
        # Optional fields
        self.patterns = ast.literal_eval(self.configuration.get("patterns", self.PATTERNS_DEFAULT))
        self.ignored_patterns = ast.literal_eval(self.configuration.get("ignored_patterns", self.IGNORED_PATTERNS_DEFAULT))
        self.allowed_trigger_types = ast.literal_eval(self.configuration.get("allowed_trigger_types", self.ALLOWED_TRIGGER_TYPES_DEFAULT))
        self.trigger_additional_data = self.configuration.get("trigger_additional_data", None)

        self.watch = None
        self.logger.debug("DirWatchTrigger started")

    def dir_watch_adapter(self):
        return self.get_adapter_by_uuid(self.dir_watch_adapter_uuid)

    def start(self):
        self.watch = self.dir_watch_adapter().add_dir_to_watch(self.trigger_engaged, self.watched_path)

    def stop(self):
        try:
            self.dir_watch_adapter().remove_dir_to_watch(self.watch)
        except Exception as e:
            self.logger.error(e)

    def trigger_engaged(self, command=None):
        "Called when a change occured and matched the file pattern"
        # Check if the event types matches
        event_details = command
        self.logger.debug("DirWatchTrigger callback_called")
        self.logger.debug("event type is:%s allowed types:%s" % (event_details.event_type, self.allowed_trigger_types,))
        # TODO Add Resetting sleep status - don't send everything, have a cool down timer
        if event_details.event_type in self.allowed_trigger_types:
            # Check if the path matches the given patterns 
            self.logger.debug("event is in allowed types")
            event_matches_path = match_path(event_details.src_path, self.patterns, self.ignored_patterns, case_sensitive=False)
            self.logger.debug("event path: %s matches pattern: %s, bool is :%s" % (event_details.src_path, self.patterns, event_matches_path))
            if event_matches_path is True:
                trigger_data = {"event_type": event_details.event_type,
                                "is_directory": event_details.is_directory,
                                LingerConstants.FILE_PATH_SRC: event_details.src_path}
                self.trigger_callback(self.uuid, trigger_data)

        # Else, do nothing, this trigger is not for us


class DirWatchTriggerFactory(lingerTriggers.LingerBaseTriggerFactory):
    """DirWatchTriggerFactory generates DirWatchTrigger instances"""
    def __init__(self):
        super(DirWatchTriggerFactory, self).__init__()
        self.item = DirWatchTrigger

    @staticmethod
    def get_instance_name():
        return "DirWatchTrigger"

    def get_fields(self):
        fields, optional_fields = super(DirWatchTriggerFactory, self).get_fields()
        fields += [("watched_path", "string"), ("dir_watch_adapter_uuid", "Adapters")]
        optional_fields += [("patterns", ('array', 'string')),
                            ("ignored_patterns", ('array', 'string')),
                            ("allowed_trigger_types", ['modified', 'created', 'moved', 'deleted']),
                            ("trigger_additional_data", "string")
                            ]

        return fields, optional_fields
