import LingerAdapters.LingerBaseAdapter as lingerAdapters 

# Operation specific imports
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging


class DirWatchEventHandler(FileSystemEventHandler):
    """Event handler for observers manged by the DirWatchAdapter"""
    def __init__(self, callback, logger):
        super(DirWatchEventHandler, self).__init__()
        self.logger = logger
        self.callback = callback


    def on_deleted(self, event):
        """Some file changed"""
        self.logger.debug("on_deleted called")
        self.callback(event)
    
    def on_moved(self, event):
        """Some file changed"""
        self.logger.debug("on_moved called")
        self.callback(event)
    
    def on_modified(self, event):
        """Some file changed"""
        self.logger.debug("on_modified called")
        self.callback(event)
    
    def on_created(self, event):
        """Some file changed"""
        self.logger.debug("on_created called")
        self.callback(event)


class DirWatchAdapter(lingerAdapters.LingerBaseAdapter):
    """DirWatchAdapter ables watching changes in directories"""

    def __init__(self, configuration):
        super(DirWatchAdapter, self).__init__(configuration)
        self.logger.debug("DirWatchAdapter started")
        self.observer = Observer()
        self.observer.start()

    def add_dir_to_watch(self, callback, path_to_watch):
        # Getting absolute path
        absolute_path_to_watch = os.path.abspath(path_to_watch)

        # TODO need here to make sure is dir. or someplace else
        # Create new event handler for the watch 
        event_handler = DirWatchEventHandler(callback, self.logger)

        # Schedule for observer
        return self.observer.schedule(event_handler, absolute_path_to_watch, recursive=False)

    def remove_dir_to_watch(self, watch):
        try:
            self.observer.unschedule(watch)
        except Exception as e:
            self.logger.error(e)

    def __del__(self):
        self.logger.debug("calling dtor")
        self.observer.unschedule_all()
        self.logger.debug("all unscheduled")
        self.observer.stop()
        self.logger.debug("stopped observer")
        self.observer.join()
        self.logger.debug("joined")

class DirWatchAdapterFactory(lingerAdapters.LingerBaseAdapterFactory):
    """DirWatchAdapterFactory generates DirWatchAdapter instances"""
    def __init__(self):
        super(DirWatchAdapterFactory, self).__init__()
        self.item = DirWatchAdapter

    def get_instance(self, configuration):
        adapter = DirWatchAdapter(configuration)
        return adapter
    
    def get_instance_name(self):
        return "DirWatchAdapter"
