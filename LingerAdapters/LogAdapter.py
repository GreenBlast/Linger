import LingerAdapters.LingerBaseAdapter as lingerAdapters 

class LogAdapter(lingerAdapters.LingerBaseAdapter):
    """LogAdapter ables logging lines to a given log"""

    def __init__(self, configuration):
        super(LogAdapter, self).__init__(configuration)
        self.logger.debug("LogAdapter started")
    
    def log(self, what_to_log):
        self.logger.info(what_to_log)

class LogAdapterFactory(lingerAdapters.LingerBaseAdapterFactory):
    """LogAdapterFactory generates LogAdapter instances"""
    def __init__(self):
        super(LogAdapterFactory, self).__init__()
        self.item = LogAdapter
    
    def get_instance_name(self):
        return "LogAdapter"