import socket
import gevent
from gevent import monkey
monkey.patch_all()

class WebServer():
    def __init__(self):
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        tcp_socket.bind(('', 12900))
        tcp_socket.listen(128)
        self.tcp_socket = tcp_socket

    def start(self):
        while True:
            new_socket, ip_port = self.tcp_socket.accept()
            # 使用协程，加快速度
            gevent.spawn(self.request_handler, new_socket, ip_port)

    def request_handler(self, socket, ip):
        # 解析浏览器请求的地址
        recv_data = socket.recv(2048)
        print(recv_data)
        recv_txt = recv_data.decode()
        log = recv_txt.find('\r\n')
        recv_split = recv_txt[:log]
        request_list = recv_split.split(' ')
        path = request_list[1]
        print(path)
        if path == '/':
            with open('login.html', 'rb') as file:
                response_body = file.read()
            socket.send(self.response_msg(response_body))
            socket.close()
        else:
            with open('.' + path, 'rb') as file:
                response_body = file.read()
            socket.send(self.response_msg(response_body))
            socket.close()

    def response_msg(self, body):
        # 服务器响应头数据拼接
        response_line = 'HTTP/1.1 200 OK\r\n'
        response_head = 'Server: LocalPython/1.1\r\n'
        response_bank = '\r\n'
        response_data = (response_line + response_head + response_bank).encode() + body
        print('1')
        return response_data


if __name__ == '__main__':
    web_start = WebServer()
    web_start.start()
