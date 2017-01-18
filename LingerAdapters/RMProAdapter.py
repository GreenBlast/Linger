"""
RMProAdapter enables controling an RMPro device
"""

# Operation specific imports
import broadlink

import LingerAdapters.LingerBaseAdapter as lingerAdapters

class RMProAdapter(lingerAdapters.LingerBaseAdapter):
    """RMProAdapter ables commanding RMPro"""

    def __init__(self, configuration):
        super(RMProAdapter, self).__init__(configuration)
        self.logger.debug("RMProAdapter started")
        self.ac_is_on = False

        # fields
        self.rmpro_ip = configuration["rmpro_ip"]
        self.rmpro_port = configuration["rmpro_port"]
        self.rmpro_mac = configuration["rmpro_mac"]

        # Setting device
        self.device = broadlink.rm(host=(self.rmpro_ip, int(self.rmpro_port)), mac=bytearray.fromhex(self.rmpro_mac))

        # Setting the base command, and comparing command on the bridge with preteached commands
        self.logger.info("RMProAdapter configured with ip=%s, port=%s", self.rmpro_ip, self.rmpro_port)
        self.logger.debug("RMProAdapter configured")


    def toggle_ac_status(self):
        """Toggling the state of the AC"""
        self.logger.debug("ac state on before toggling is:%s", self.ac_is_on)
        self.ac_is_on = not self.ac_is_on

    def start_ac(self):
        """Starting the AC"""
        if not self.ac_is_on:
            self.toggle_ac_status()

    def stop_ac(self):
        """Stopping the AC"""
        if self.ac_is_on:
            self.toggle_ac_status()

    def get_temperature(self):
        """Getting temperature of the device"""
        self.device.auth()
        answer = self.device.check_temperature()

        return answer

class RMProAdapterFactory(lingerAdapters.LingerBaseAdapterFactory):
    """RMProAdapterFactory generates RMProAdapter instances"""
    def __init__(self):
        super(RMProAdapterFactory, self).__init__()
        self.item = RMProAdapter

    @staticmethod
    def get_instance_name():
        """Returns instance name"""
        return "RMProAdapter"

    def get_fields(self):
        """Returns the fields used by the instance"""
        fields, optional_fields = super(RMProAdapterFactory, self).get_fields()
        fields += [('rmpro_ip', "string"), ('rmpro_port', "integer"), ('rmpro_mac', "string")]
        return (fields, optional_fields)
