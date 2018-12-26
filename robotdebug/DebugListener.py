import os
import shutil
import textwrap
import threading
from enum import Enum
import time
import zmq

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def _format_print(text, end=os.linesep):
    termlen = shutil.get_terminal_size().columns
    print(textwrap.shorten(text, width=termlen, placeholder='...'), end=end)


def _print_divider(div='-'):
    print(div * shutil.get_terminal_size().columns)


def _print_result(name, result):
    termlen = shutil.get_terminal_size().columns
    ftext = textwrap.shorten(name, width=termlen-10, placeholder='... ')
    color = bcolors.OKGREEN if result == 'PASS' else bcolors.FAIL
    fresult = '[{}{}{}]'.format(color, result, bcolors.ENDC)
    ftext = '{}{:>{width}}'.format(ftext, fresult, width=termlen - len(fresult) - 1)
    print(ftext)


def _print_keyword(name, args, result):
    _print_result('  {}'.format(name), result)


class DebugListener(object):

    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self, *args):
        """
        Local debugging only:
            robot --listener DebugListener

        Using debug server running on <url>:<port>
            robot --listener DebugListener:<url>:<port>
        """
        if len(args) == 2:
            self._use_debug_server = True
            self._addr = 'tcp://{}:{}'.format(args[0], args[1])
            self._is_connected = False
            self._connect(timeout=5)

        else:
            self._use_debug_server = False


    def _connect(self, timeout):
        """

        """
        print('listener connecting to {}'.format(self._addr))
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.PAIR)
        self._socket.connect(self._addr)
        self._handshake(timeout)


    def _handshake(self, timeout):
        """

        """
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
        """

        """
        if self._use_debug_server and self._is_connected:
            msg = {
                'topic': 'start suite',
                'name': name,
                'longname': attributes['longname'],
            }
            self._socket.send_json(msg)

        else:
            _print_divider()
            _format_print(attributes['longname'])
            _print_divider()


    def end_suite(self, name, attributes):
        """

        """
        if self._use_debug_server and self._is_connected:
            msg = {
                'topic': 'end suite',
                'name': name,
                'longname': attributes['longname'],
            }
            self._socket.send_json(msg)

        else:
            _print_divider()
            _print_result(attributes['longname'], attributes['status'])
            _print_divider()


    def start_test(self, name, attributes):
        """

        """
        if self._use_debug_server and self._is_connected:
            msg = {
                'topic': 'start test',
                'name': name,
                'longname': attributes['longname'],
            }
            self._socket.send_json(msg)

        else:
            _format_print(attributes['longname'])



    def end_test(self, name, attributes):
        """

        """
        if self._use_debug_server and self._is_connected:
            msg = {
                'topic': 'end test',
                'name': name,
                'longname': attributes['longname'],
            }
            self._socket.send_json(msg)

        else:
            _print_result(attributes['longname'], attributes['status'])


    def start_keyword(self, name, attributes):
        """

        """
        if self._use_debug_server and self._is_connected:
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

        else:
            self._handle_local_debug()


    def _handle_local_debug(self):
        """

        """
        pass


    def end_keyword(self, name, attributes):
        """

        """
        if self._use_debug_server and self._is_connected:
            msg = {
                'topic': 'end keyword',
                'name': name,
                'type': attributes['type'],
                'kwname': attributes['kwname'],
                'libname': attributes['libname'],
                'args': attributes['args']
            }
            self._socket.send_json(msg)

        else:
            _print_keyword(attributes['kwname'], attributes['args'], attributes['status'])


    def close(self):
        """

        """
        if self._use_debug_server and self._is_connected:
            msg = {
                'topic': 'close',
            }
            self._socket.send_json(msg)

        else:
            pass



if __name__ == '__main__':
    DebugListener('localhost', 5555)
