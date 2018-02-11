import network
import utime
import config
import logger

_log = logger.get_logger()
_config = config.get_config()
_ssid = _config.get_ssid()
_password = _config.get_password()
_wlan = None

def is_connected():
    return _wlan.isconnected()

def wifi_connect(essid, password):
    # Connect to the wifi. Based on the example in the micropython
    # documentation.
    _wlan = network.WLAN(network.STA_IF)
    _wlan.active(True)
    if not _wlan.isconnected():
        _log.info('connecting to network ' + essid + '...')
        _wlan.connect(essid, password)
        # connect() appears to be async - waiting for it to complete
        while not _wlan.isconnected():
            _log.info('waiting for connection...')
            utime.sleep(4)
            _log.info('checking connection...')
        _log.info('Wifi connect successful, network config: %s' % repr(_wlan.ifconfig()))
    else:
        # Note that connection info is stored in non-volatile memory. If
        # you are connected to the wrong network, do an explicity disconnect()
        # and then reconnect.
        _log.info('Wifi already connected, network config: %s' % repr(_wlan.ifconfig()))

def wifi_disconnect():
    # Disconnect from the current network. You may have to
    # do this explicitly if you switch networks, as the params are stored
    # in non-volatile memory.
    wlan = network.WLAN(network.STA_IF)
    if wlan.isconnected():
        _log.info("Disconnecting...")
        wlan.disconnect()
    else:
        _log.info("Wifi not connected.")

def disable_wifi_ap():
    # Disable the built-in access point.
    wlan = network.WLAN(network.AP_IF)
    wlan.active(False)
    _log.info('Disabled access point, network status is %s' %
          wlan.status())
          
def init():
    wifi_connect(_ssid, _password)

