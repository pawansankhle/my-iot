import machine
import ubinascii
import logger


log = logger.get_logger()

class Config(object):
    CONFIG = {
        "broker": "172.20.10.2",
        "sensor_pin": 0, 
        "client_id": b"esp8266_" + ubinascii.hexlify(machine.unique_id()),
        "topic": b"home",
        "port": 1883,
        "ssid": "iPhone",
        "password": "12345678"
    }

    def __init__(self):
       self._load_config()

    def _load_config(self):
        import ujson as json
        try:
            with open("/config.json") as f:
                self.config = json.loads(f.read())
        except (OSError, ValueError):
            log.error("Couldn't load /config.json")
            self._save_config()
        else:
            self.CONFIG.update(self.config)
            log.info("Loaded config from /config.json")

    def _save_config(self):
        import ujson as json
        try:
            with open("/config.json", "w") as f:
                f.write(json.dumps(self.CONFIG))
        except OSError:
            log.error("Couldn't save /config.json")
    
    def get_ssid(self):
        return self.config['ssid']

    def get_password(self):
        return self.config['password']

    def get_broker(self):
        return self.config['broker']

    def get_client_id(self):
        return self.config['client_id']

    def get_topic(self):
        return self.config['topic']

    def get_port(self):
        return self.config['port']
    
_config = None


def initialize_config():
    global _config
    if _config!=None:
         raise Exception("config was already initialized!")
    _config = Config()

def get_config():
    global _config
    if _config!=None:
        return _config
    else:
        raise Exception("Config was not yet initialized!")
