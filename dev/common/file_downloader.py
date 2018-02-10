import uos as os
import usocket as socket
import logger
import urequests

_logger = logger.initialize_logging('micro.log')
import config
config.initialize_config()
_config = config.get_config()


# todo: https

# def http_get_async(url):
    # _, _, host, path = url.split('/', 3)
    # if ':' in host:
    #     host, port = host.split(':')
    # else:
    #     port = 80
    # addr = socket.getaddrinfo(host, port)[0][-1]
    # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s.connect(addr)
    # s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host),
    #              'utf8'))
    # started = False
    # header_str = b''
    # headers = {}
    # while True:
    #     data = s.recv(1000)
    #     if data:
    #         body_bytes = data
    #         if not started and b'HTTP' in body_bytes:
    #             if b'301' in body_bytes:
    #                 print(body_bytes)
    #                 for u in body_bytes.split(b'\r\n'):
    #                     if b'Location:' in u:
    #                         url = str(u).split('Location: ')[1].replace("'", "").strip()
                            
    #                         # print(url)
    #                         # start(url)
                            
    #             started = True
    #             continue
    #         buffer = header_str + body_bytes
            
    #         if not headers and not b'\r\n\r\n' in buffer:
    #             header_str += body_bytes
    #             continue
    #         if b'\r\n\r\n' in buffer:
    #             headers, body_bytes = buffer.split(b'\r\n\r\n')
            
            # if body_bytes:
            #     yield body_bytes
        # else:
        #     break


def http_get(url):
    response = b''
    try:
        r = urequests.request('GET', url)
        response += r.content
        # while True:
        #     file_bytes = get.send(None)
        #     response += file_bytes
    except Exception as ex:
        print(ex)

    response_str = str(response, 'utf-8')
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


def http_get_to_file(url, path):
    ensure_dirs(path)
    print(path)
    with open(path, 'w') as outfile:
        try:
            get = http_get(url)
            print(get)
            # while True:
            #     file_bytes = get.send(None)
            outfile.write(get)
        except Exception as ex:
            print(ex)
            outfile.close()

def start(url='https://raw.githubusercontent.com/pawansankhle/my-iot/master/dev/{}/update.json'.format(_config.get_client_id())):
    try:
        import ujson as json
        res = http_get(url)
        response = json.loads(res)
        for file in response['files']:
            path = file['path']
            url = 'https://raw.githubusercontent.com/pawansankhle/my-iot/master/dev/{}/{}'.format(_config.get_client_id(), path)
            http_get_to_file(url, path)
    except Exception as ex:
            print(ex)


if __name__ == '__main__':
    start()