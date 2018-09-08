import time
import zmq


class DebugListener(object):

    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self, *args):
        """

        """
        assert len(args) >= 2
        self._addr = 'tcp://{}:{}'.format(args[0], args[1])
        self._is_connected = False
        self._connect(timeout=5)


    def _connect(self, timeout):
        print('listener connecting to {}'.format(self._addr))
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.PAIR)
        self._socket.connect(self._addr)
        self._handshake(timeout)


    def _handshake(self, timeout):
        self._socket.send_json({'topic': 'request_handshake'})

        for _ in range(0, timeout):
            try:
                response = self._socket.recv_json(flags=zmq.NOBLOCK)
                if response['topic'] == 'response_handshake':
                    self._is_connected = True
                    break

            except zmq.ZMQError:
                pass

            except:
                break

    def start_suite(self, name, attributes):
        if self._is_connected:
            msg = {
                'topic': 'start suite',
                'name': name,
                'longname': attributes['longname'],
            }
            self._socket.send_json(msg)


    def end_suite(self, name, attributes):
        if self._is_connected:
            msg = {
                'topic': 'end suite',
                'name': name,
                'longname': attributes['longname'],
            }
            self._socket.send_json(msg)


    def start_test(self, name, attributes):
        if self._is_connected:
            msg = {
                'topic': 'start test',
                'name': name,
                'longname': attributes['longname'],
            }
            self._socket.send_json(msg)


    def end_test(self, name, attributes):
        if self._is_connected:
            msg = {
                'topic': 'end test',
                'name': name,
                'longname': attributes['longname'],
            }
            self._socket.send_json(msg)


    def start_keyword(self, name, attributes):
        if self._is_connected:
            msg = {
                'topic': 'start keyword',
                'name': name,
                'type': attributes['type'],
                'kwname': attributes['kwname'],
                'libname': attributes['libname'],
                'args': attributes['args']
            }
            self._socket.send_json(msg)
            msg = self._socket.recv_json()


    def end_keyword(self, name, attributes):
        if self._is_connected:
            msg = {
                'topic': 'end keyword',
                'name': name,
                'type': attributes['type'],
                'kwname': attributes['kwname'],
                'libname': attributes['libname'],
                'args': attributes['args']
            }
            self._socket.send_json(msg)


    def close(self):
        if self._is_connected:
            msg = {
                'topic': 'close',
            }
            self._socket.send_json(msg)



if __name__ == '__main__':
    DebugListener('localhost', 5555)
