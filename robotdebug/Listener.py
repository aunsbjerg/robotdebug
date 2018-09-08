import time
import zmq


class Listener(object):

    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self, *args):
        """

        """
        assert len(args) >= 2
        host = args[0]
        port = int(args[1])

        context = zmq.Context()
        self._socket = context.socket(zmq.PAIR)
        self._socket.connect("tcp://{}:{}".format(host, port))

        print("listener connecting to {}:{}".format(host, port))


    def start_suite(self, name, attributes):
        msg = {
            'topic': 'start suite',
            'name': name,
            'longname': attributes['longname'],
        }
        self._socket.send_json(msg)


    def end_suite(self, name, attributes):
        msg = {
            'topic': 'end suite',
            'name': name,
            'longname': attributes['longname'],
        }
        self._socket.send_json(msg)


    def start_test(self, name, attributes):
        msg = {
            'topic': 'start test',
            'name': name,
            'longname': attributes['longname'],            
        }
        self._socket.send_json(msg)


    def end_test(self, name, attributes):
        msg = {
            'topic': 'end test',
            'name': name,
            'longname': attributes['longname'],
        }
        self._socket.send_json(msg)


    def start_keyword(self, name, attributes):
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
        msg = {
            'topic': 'close',
        }
        self._socket.send_json(msg)



class TestServer(object):

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
                
    
import sys

if __name__ == '__main__':
    try:
        if sys.argv[1] == 'server':
            server = TestServer("localhost", 5555)
            server.run()

        elif sys.argv[1] == 'client':
            Listener("localhost", 5555)

        else:
            print("exiting")
            exit(1)

    except KeyboardInterrupt:
        pass

    finally:
        server.close()


    