import asyncio


class ClientServerProtocol(asyncio.Protocol):
    metric_storage = {}

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        resp = self.process_data(data.decode('utf-8'))
        self.transport.write(resp.encode('utf-8'))

    # обработка запросов
    @staticmethod
    def process_data(data):
        reply_pattern = 'ok'
        request = data.strip('\n').split()
        if request[0] == 'put':
            if request[1] not in ClientServerProtocol.metric_storage:
                ClientServerProtocol.metric_storage[request[1]] = '\n' + ' '.join(request[1:])
            else:
                ClientServerProtocol.metric_storage[request[1]] += '\n' + ' '.join(request[1:])
            return reply_pattern + '\n\n'
        elif request[0] == 'get':
            if request[1] == '*':
                for i in ClientServerProtocol.metric_storage:
                    reply_pattern += ClientServerProtocol.metric_storage[i]
                return reply_pattern + '\n\n'
            else:
                if request[1] not in ClientServerProtocol.metric_storage:
                    return reply_pattern + '\n\n'
                else:
                    return reply_pattern + ClientServerProtocol.metric_storage[request[1]] + '\n\n'
        else:
            return 'error\nwrong command\n\n'


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientServerProtocol,
        host,
        port
    )

    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
