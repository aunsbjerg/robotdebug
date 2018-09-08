import shutil
import sys
import subprocess
import time

if __name__ == '__main__':
    exitcode = 0

    try:
        p1 = subprocess.Popen(['pipenv', 'run', 'python', 'robotdebug/DebugServer.py', 'localhost', '5555'])

        time.sleep(2)
        p2 = subprocess.Popen(['pipenv', 'run', 'robot', '--listener', 'DebugListener:localhost:5555',
            '--pythonpath', 'robotdebug', '--outputdir', 'results', 'tests/robot/demo.robot'])

        p2.communicate()
        shutil.rmtree('results')

    except Exception as exc:
        print(exc)
        exitcode = 1

    finally:
        p1.terminate()
        p2.terminate()
        exit(exitcode)
