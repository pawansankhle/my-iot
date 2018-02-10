# Writer interface over umqtt API.

from umqtt.robust import MQTTClient
import json
import time
import webrepl
import machine
import logger
import config

# initialize logger 
_log = logger.get_logger()
_config = config.get_config()
_broker = _config.get_broker()
_port = _config.get_port()
_client_id = _config.get_client_id()
_topic = _config.get_topic()


# These defaults are overwritten with the contents of /config.json by load_config()
def _connect():
    try:
        global client
        _log.info("Connecting to %s:%s" % (_broker, _port))
        client = MQTTClient(_client_id, _broker)
        client.connect()
        _log.info("Connection successful")
    except Exception as ex:
        _log.error("error in _connect " + str(ex))

def on_next(x):
    try:
        global client
        print()
        data = bytes(json.dumps(x), 'utf-8')
        _log.info(_topic +" " + _client_id + " " + json.dumps(x))
        client.publish('{}/{}'.format(_topic,
                                          _client_id),
                                          data)
    except Exception as ex:
        _log.error("error in on_next" + str(ex))

def on_completed():
    global client
    _log.info("mqtt_completed, disconnecting")
    client.disconnect()

def on_error(e):
    global client
    _log.error("mqtt on_error: %s, disconnecting" %e)
    client.disconnect()

def init():
    _connect()
    

if __name__ == '__main__':
    init()

