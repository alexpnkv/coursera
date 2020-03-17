# клиент для отправки и приема метрик

import socket
import time


class ClientError(Exception):
    pass


class Client:

    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sock = socket.create_connection(
            (self.host, self.port),
            self.timeout)

    def send_message(self, message):
        try:
            self.sock.sendall(message.encode('utf-8'))
            server_reply = self.sock.recv(1024)
        except Exception:
            raise ClientError
        return server_reply.decode('utf-8')

    @staticmethod
    def to_dict(data):
        metric_dict = {}
        metric_list = data.split('\n')
        for i in range(1, len(metric_list) - 2):
            if metric_list[i].split()[0] not in metric_dict:
                metric_dict[metric_list[i].split()[0]] = [(int(metric_list[i].split()[2]),
                                                           float(metric_list[i].split()[1]))]
            else:
                metric_dict[metric_list[i].split()[0]].append((int(metric_list[i].split()[2]),
                                                               float(metric_list[i].split()[1])))
        for i in metric_dict:
            metric_dict[i].sort()
        return metric_dict

    def put(self, metric_name, metric_value, timestamp=int(time.time())):
        send_metric = f'put {metric_name} {float(metric_value)} {timestamp}\n'
        server_reply = self.send_message(send_metric)

        if server_reply == "error\nwrong command\n\n":
            raise ClientError
        if server_reply == "ok\n\n":
            print('hey!!!!!')

    def get(self, metric_name):
        message = f'get {metric_name}\n'
        server_reply = self.send_message(message)

        if server_reply == "error\nwrong command\n\n":
            raise ClientError

        metric_dict = self.to_dict(server_reply)

        return metric_dict

    def close(self):
        self.sock.close()


client = Client("127.0.0.1", 8888, timeout=15)
client.put("palm.cpu", 10.6, timestamp=1501864247)
