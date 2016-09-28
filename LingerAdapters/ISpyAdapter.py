import LingerAdapters.LingerBaseAdapter as lingerAdapters 

# Operation specific imports
import requests
import threading

class ISpyAdapter(lingerAdapters.LingerBaseAdapter):
    """ISpyAdapter ables commanding Ispy"""

    # Don't touch, hardcoded commands for Ispy Http control
    BASIC_COMMAND = r"http://%s:%s/"
    ALL_OFF_COMMAND = r"alloff"
    START_DEV_COMMAND = r"bringonline?ot=%s&oid=%s"
    GRAB_SNAPSHOT_COMMAND = r"snapshot?oid=%s"
    ALERTS_ON_COMMAND = r"alerton"
    ALERTS_OFF_COMMAND = r"alertoff"
    CAM_DEV = 1
    CAM_DEV_TYPE = 0
    MIC_DEV = 1
    MIC_DEV_TYPE = 1
    OK_ANSWER = 'OK'
    OK_RUNNING_ANSWER = r"iSpy server is running"

    def __init__(self, configuration):
        super(ISpyAdapter, self).__init__(configuration)
        self.logger.debug("ISpyAdapter started")
        self.lock = threading.Lock()


        # fields
        self.ispy_ip = configuration["ispy_ip"]
        self.ispy_port = configuration["ispy_port"]

        self.base_command = self.BASIC_COMMAND % (self.ispy_ip, self.ispy_port,)
        self.logger.info("ISpyAdapter configured with ip=%s, port=%s" % (self.ispy_ip, self.ispy_port,))
        self.logger.debug("ISpyAdapter configured")

    def shutdown(self):
        self.logger.info("Shutdown engaged")
        self._send_command(self.ALL_OFF_COMMAND)

    def start(self):
        self.logger.info("Start engaged")
        self._send_command(self.START_DEV_COMMAND % (self.MIC_DEV_TYPE, self.MIC_DEV))

    def cam_on(self):
        self.logger.info("Camera on engaged")
        self._send_command(self.START_DEV_COMMAND % (self.CAM_DEV_TYPE, self.CAM_DEV))

    def grab_snapshot(self):
        self.logger.info("Grabbing snapshot")
        self._send_command_running_response(self.GRAB_SNAPSHOT_COMMAND % (self.CAM_DEV))

    def alerts_on(self):
        self.logger.info("Setting alerts on")
        self._send_command(self.ALERTS_ON_COMMAND)

    def alerts_off(self):
        self.logger.info("Setting alerts off")
        self._send_command(self.ALERTS_OFF_COMMAND)

    def _send_command(self,command):
        with self.lock:
            answer = requests.get(self.base_command + command)
            if answer.status_code == 200 and answer.content == self.OK_ANSWER:
                self.logger.info("Success on command: %s" % (self.base_command + command))
            else:
                self.logger.info("Failure on command: %s" % (self.base_command + command))

    def _send_command_running_response(self,command):
        with self.lock:
            answer = requests.get(self.base_command + command)
            if answer.status_code == 200 and answer.content == self.OK_RUNNING_ANSWER:
                self.logger.info("Success on command: %s" % (self.base_command + command))
            else:
                self.logger.info("Failure on command: %s" % (self.base_command + command))

class ISpyAdapterFactory(lingerAdapters.LingerBaseAdapterFactory):
    """ISpyAdapterFactory generates ISpyAdapter instances"""
    def __init__(self):
        super(ISpyAdapterFactory, self).__init__()
        self.item = ISpyAdapter

    def get_instance_name(self):
        return "ISpyAdapter"

    def get_fields(self):
        fields, optional_fields = super(ISpyAdapterFactory, self).get_fields()
        fields += [('ispy_ip',"string"), ('ispy_port',"integer")]
        return (fields,optional_fields)
