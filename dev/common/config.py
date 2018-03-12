import machine
import ubinascii
import logger


log = logger.get_logger()

class Config(object):
    CONFIG = {
        "version": "0.0.0",
        "broker" : "m12.cloudmqtt.com",
        "broker_username" : "ukkwldeo",
        "broker_password": "2RVrpiGaqfX-",
        "sensor_pin": 0, 
        "client_id": b"esp8266_" + ubinascii.hexlify(machine.unique_id()),
        "topic": b"home/light",
        "port": 10063,
        "ssid": "iPhone",
        "password": "12345678",
        "github_path": "https://raw.githubusercontent.com/pawansankhle/my-iot/master/dev/"
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

    def update_app_version(self, version):
        self.CONFIG['version'] = version
        self._save_config()
    
    def get_ssid(self):
        return self.config['ssid']

    def get_password(self):
        return self.config['password']

    def get_broker(self):
        return self.config['broker']

    def get_broker_username(self):
        return self.config['broker_username']

    def get_broker_password(self):
        return self.config['broker_password']

    def get_client_id(self):
        return self.config['client_id']

    def get_topic(self):
        return self.config['topic']

    def get_port(self):
        return self.config['port']

    def get_github_repo(self):
        return self.config['github_path']
    
    def get_version(self):
        return self.config['version']
    
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
