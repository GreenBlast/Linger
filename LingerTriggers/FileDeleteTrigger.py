import LingerConstants
import LingerTriggers.DirWatchTrigger as dirWatchTrigger

# Operation specific imports
from pathtools.patterns import match_path_against
import os


class FilePathNotValidException(Exception):
    """FilePathNotValidException is raised when the trigger file location is not valid"""
    pass        


class FileDeleteTrigger(dirWatchTrigger.DirWatchTrigger):
    """Trigger watches for changes in a directory"""

    ALLOWED_TRIGGER_TYPES_DEFAULT = "[\'deleted\']"

    def __init__(self, configuration):
        super(FileDeleteTrigger, self).__init__(configuration)

        self.trigger_file_name = self.configuration["trigger_file_name"]

        self.trigger_file_fullpath = self.watched_path + os.sep + self.trigger_file_name 
        self.validate_file_location()

        # Only 'delete' is allowed for FileDeleteTrigger
        self.allowed_trigger_types = self.ALLOWED_TRIGGER_TYPES_DEFAULT

        self.logger.debug("FileDeleteTrigger started")

    def start(self):
        self.create_trigger_file()
        super(FileDeleteTrigger, self).start()

    def stop(self):
        super(FileDeleteTrigger, self).stop()
        self.delete_trigger_file()

    def create_trigger_file(self):
        self.validate_file_location()
        trigger_file = open(self.trigger_file_fullpath, 'w')
        trigger_file.close()

    def validate_file_location(self):
        """ Makes sure that the trigger file can be created"""
        # Check the if the directory to watch exist
        if os.path.isdir(self.watched_path) is False:
            raise FilePathNotValidException("Directory %s was not found " %(self.watched_path, ))
        
        # Check that the path for the file is not a directory
        if os.path.isdir(self.trigger_file_fullpath) is True:
            raise FilePathNotValidException("Trigger file %s is an already exist directory " %(self.trigger_file_fullpath, ))

        # Check that the file doesn't exist already    
        if os.path.isfile(self.trigger_file_fullpath) is True:
            raise FilePathNotValidException("Trigger file %s already exist " %(self.trigger_file_fullpath, ))

    def delete_trigger_file(self):
        try:
            os.unlink(self.trigger_file_fullpath)
        except:
            pass

    def trigger_engaged(self, command=None):
        "Called when a change occured and matched the file pattern"
        # Check if the event types matches
        event_details = command
        self.logger.debug("FileDeleteTrigger callback_called")
        self.logger.debug("event type is:%s allowed types:%s" % (event_details.event_type, self.allowed_trigger_types,))

        if event_details.event_type in self.allowed_trigger_types:
            # Check if the path matches the given patterns 
            self.logger.debug("event is in allowed types")
            event_matches_path = match_path_against(event_details.src_path, [self.trigger_file_fullpath], case_sensitive=False)
            self.logger.debug("event path: %s matches pattern: %s, bool is :%s" % (event_details.src_path, self.trigger_file_fullpath, event_matches_path))
            if event_matches_path is True:
                trigger_data = {"event_type": event_details.event_type,
                                "is_directory": event_details.is_directory,
                                LingerConstants.FILE_PATH_SRC: event_details.src_path}

                if self.trigger_additional_data:
                    trigger_data[LingerConstants.TEXT_DATA] = self.trigger_additional_data
                self.trigger_callback(self.uuid, trigger_data)
                # after callback, regenerate the file
                self.create_trigger_file()

        # Else, do nothing, this trigger is not for us


class FileDeleteTriggerFactory(dirWatchTrigger.DirWatchTriggerFactory):
    """FileDeleteTriggerFactory generates FileDeleteTrigger instances"""
    def __init__(self):
        super(FileDeleteTriggerFactory, self).__init__()
        self._self = self
        self.item = FileDeleteTrigger

    def get_instance_name(self):
        return "FileDeleteTrigger"

    def get_fields(self):
        fields, optional_fields = super(FileDeleteTriggerFactory, self).get_fields()
        fields += [("trigger_file_name", "string")]
        optional_fields.remove(("allowed_trigger_types", ['modified', 'created', 'moved', 'deleted']))
        return fields, optional_fields
