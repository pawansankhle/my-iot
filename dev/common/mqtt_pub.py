# Writer interface over umqtt API.
import json
import logger
import config

# initialize logger 
_log = logger.get_logger()
_config = config.get_config()
_port = _config.get_port()
_client_id = _config.get_client_id()
_topic = _config.get_topic()

client = None
def publish(topic, client_id, data):
    global client
    _log.info("going to publish" + topic +"/" + client_id + " " + data)
    client.publish('{}/{}'.format(topic,client_id),data)


def on_pub(x, topic = _topic, client_id = _client_id):
    import mqtt
    try:
        client = mqtt.get_connection()
        data = bytes(json.dumps(x), 'utf-8')
        if client != None:
            publish(topic, client_id, data)
        else:
            mqtt._connect()
            client = mqtt.get_connection()
            publish(topic, client_id, data)
    except Exception as ex:
        _log.error("error in on_next" + str(ex))
