import uos as os
# import usocket as socket
import logger
import urequests
import config

_logger = logger.get_logger()
_config = config.get_config()

def http_get(url):
    response = b''
    try:
        r = urequests.request('GET', url)
        response += r.content
    
    except Exception as ex:
        _logger.error(' Error in http_get '+ str(ex))

    response_str = str(response, 'utf-8')
    # print(response_str)
    return response_str


def ensure_dirs(path):
    split_path = path.split('/')
    if len(split_path) > 1:
        for i, fragment in enumerate(split_path):
            parent = '/'.join(split_path[:-i])
            try:
                os.mkdir(parent)
            except OSError:
                pass

def remove_file(path):
    if path != None:
        try:
            os.remove(path)
        except OSError:
            pass


def http_get_to_file(url, path):
    # ensure_dirs(path)
    # remove_file(path)
    with open(path, 'w') as outfile:
        try:
            get = http_get(url)
            if get:
                outfile.write(get)

        except Exception:
            outfile.close()

def get_file_path(path):
    return path.split("/")[-1]

def is_update_require(version):
   return version == _config.get_version()

def is_connected():
    import network
    _wlan = network.WLAN(network.STA_IF)
    try:
        return _wlan.isconnected()
    except:
        return False

def reset_device():
    import machine
    _logger.info('going to reset device...')
    machine.reset()

def start(url='https://raw.githubusercontent.com/pawansankhle/my-iot/master/dev/{}/update.json'.format(_config.get_client_id())):
    try:
        _logger.info('cheking for update...')
        import ujson as json
        while is_connected():
            res = http_get(url)
            response = json.loads(res)
            version = response['version']
            if not is_update_require(version):
                for file in response['files']:
                    path = file['path']
                    url = 'https://raw.githubusercontent.com/pawansankhle/my-iot/master/dev/{}'.format(path)
                    _logger.info('going to update file {}...'.format(path))
                    http_get_to_file(url, get_file_path(path))
                _config.update_app_version(version)
                reset_device()
            else:
                _logger.info('no update required...')
            break
        else:
            _logger.info('update failed wifi not connected...')
    except Exception as ex:
        _logger.error(' Error in @start '+ str(ex))


if __name__ == '__main__':
    start()