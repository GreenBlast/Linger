import LingerTriggers.LingerBaseTrigger as lingerTriggers

# Operation specific imports
from datetime import datetime, timedelta
from apscheduler.jobstores.base import JobLookupError


class OnStart(lingerTriggers.LingerBaseTrigger):
    """
        Trigger that is doing an action on startup
    """
    def __init__(self, configuration):
        super(OnStart, self).__init__(configuration)
        self.scheduled_job = None
        self.is_started = False
        # Fields

        # Optional fields

        self.logger.debug("OnStart initialized")

    def trigger_engaged(self, event_details=None):
        self.trigger_callback(self.uuid, event_details)

    def start(self):
        if not self.is_started:
            self.is_started = True
            self.scheduled_job = self.scheduler.add_job(self.trigger_engaged,'date', run_date=datetime.now() + timedelta(0, 5))

    def stop(self):
        if self.scheduled_job != None:
            try:
                self.scheduled_job.remove()
            except JobLookupError as e:
                pass

class OnStartFactory(lingerTriggers.LingerBaseTriggerFactory):
    """OnStartFactory generates OnStart instances"""
    def __init__(self):
        super(OnStartFactory, self).__init__()
        self.item = OnStart

    def get_instance_name(self):
        return "OnStartTrigger"

    def get_fields(self):
        fields, optional_fields = super(OnStartFactory, self).get_fields()

        return (fields, optional_fields)
