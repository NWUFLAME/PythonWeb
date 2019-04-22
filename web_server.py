import socket
import re
import sys

import gevent
from gevent import monkey

monkey.patch_all()

method = None


class WSGIServer(object):
    def __init__(self, port):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(('', port))
        self.server_socket.listen(128)


    def set_response_headers(self, status, headers):
        self.status = status
        self.headers = headers


    def serve(self, client_socket):
        content = client_socket.recv(1024)
        if content:
            content = content.decode('utf-8')
            request_lines = content.splitlines()
            request_url = re.search(r'(/\S*)', request_lines[0]).group(1)
            print(request_url)
            d = dict()
            if '?' in request_url:
                index = request_url.index('?')

                params = request_url[index + 1:]
                params = params.split('&')

                for param in params:
                    key, value = param.split('=')
                    d[key] = value
                request_url = request_url[:index]
            if request_url == '/':
                request_url = '/index.html'
            elif request_url.endswith('/'):
                request_url=request_url[:len(request_url)-1]

            try:
                response = 'HTTP/1.1 200 OK\r\n\r\n'
                if request_url.startswith("/api"):
                    env = dict(url=request_url, params=d)
                    html_content = method(env, self.set_response_headers).encode('utf-8')
                    response = 'HTTP/1.1 %s\r\n' % self.status
                    for header in self.headers:
                        response += '%s: %s\r\n' % (header[0], header[1])
                    response += '\r\n'
                else:
                    with open( './static'+request_url, 'rb') as f:
                        html_content = f.read()
            except Exception as e:
                print(e)
                response = 'HTTP/1.1 404 NOT FOUND\r\nContent-Type: text/html; charset=utf-8\r\n\r\n<h1>你要的内容不存在!</h1>'
                client_socket.send(response.encode('utf-8'))
            else:
                client_socket.send(response.encode('utf-8'))
                client_socket.send(html_content)
        else:
            pass
            # print('客户端请求断开连接')
        client_socket.close()


    def run(self):
        while True:
            client_socket, client_addr = self.server_socket.accept()
            gevent.spawn(self.serve, client_socket)
        server_socket.close()


def main(port):
    server = WSGIServer(port)
    global method
    framework = __import__("wsgi")
    method = getattr(framework, "mapper")
    server.run()


if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(int(sys.argv[1]))
