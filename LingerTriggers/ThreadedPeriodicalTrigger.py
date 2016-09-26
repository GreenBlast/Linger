import LingerTriggers.LingerBaseTrigger as lingerTriggers

# Operation specific imports
import threading

class ThreadedPeriodicalTrigger(lingerTriggers.LingerBaseTrigger):
    """
        Trigger that its watch action is in a thread
        Probably shouldn't use this trigger, as it openes a new thread for each trigger and it might be performance heavy
        Should use the Linger interval ability
    """
    def __init__(self, configuration):
        super(ThreadedPeriodicalTrigger, self).__init__(configuration)
        self.thread_worker = None
        self.stop_event = None
        # Fields
        self.interval = float(self.configuration["intervalSec"])

        # Optional fields

        self.logger.debug("ThreadedPeriodicalTrigger initialized")

    def trigger_check_condition(self):
        self.logger.debug("Should check here for trigger conditions")
        return (False, None)

    def trigger_engaged(self, event_details):
        self.trigger_callback(self.uuid, event_details)

    def work_thread(self, stop_event):
        self.logger.debug("Entered work thread")
        while (not stop_event.is_set()):
            should_trigger, event_details = self.trigger_check_condition()
            if should_trigger:
                self.trigger_engaged(event_details)
            stop_event.wait(self.interval)

    def start(self):
        self.stop_event = threading.Event()
        self.thread_worker = threading.Thread(target=self.work_thread, args=(self.stop_event, ))
        self.thread_worker.daemon = True
        self.thread_worker.start()

    def stop(self):
        try:
            self.stop_event.set()
        except Exception, e:
            self.logger.error(e)

class ThreadedPeriodicalTriggerFactory(lingerTriggers.LingerBaseTriggerFactory):
    """ThreadedPeriodicalTriggerFactory generates ThreadedPeriodicalTrigger instances"""
    def __init__(self):
        super(ThreadedPeriodicalTriggerFactory, self).__init__()
        self.item = ThreadedPeriodicalTrigger

    def get_instance_name(self):
        return "ThreadedPeriodicalTrigger"

    def get_fields(self):
        fields, optional_fields = super(ThreadedPeriodicalTriggerFactory, self).get_fields()
        fields +=[("intervalSec","number")]

        return (fields,optional_fields)
