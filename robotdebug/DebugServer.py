import time
import zmq

class DebugServer(object):

    def __init__(self, *args):
        assert len(args) >= 2
        host = '*'
        port = int(args[1])
        self._addr = 'tcp://{}:{}'.format(host, port)
        print('serving on {}'.format(self._addr))

        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.PAIR)
        self._socket.bind(self._addr)


    def close(self):
        try:
            self._socket.close()
            self._context.term()

        except:
            pass


    def run(self):
        while True:
            msg = self._socket.recv_json()

            if msg['topic'] == 'start keyword':
                print(msg)
                input()
                self._socket.send_json(msg)

            if msg['topic'] == 'close':
                self.close()
                break

            time.sleep(0.050)


if __name__ == '__main__':
    try:
        server = DebugServer("localhost", 5555)
        server.run()

    except KeyboardInterrupt:
        pass

    finally:
        server.close()

