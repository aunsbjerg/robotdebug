import os
import sys
import subprocess
import time

if __name__ == '__main__':
    exitcode = 0

    try:
        p1 = subprocess.Popen(['pipenv', 'run', 'python', 'robotdebug/Listener.py', 'server', 'localhost', '5555'])

        time.sleep(1)
        p2 = subprocess.Popen(['pipenv', 'run', 'robot', '--listener', 'Listener:localhost:5555', 
            '--pythonpath', 'robotdebug', '--outputdir', 'results', 'robotdebug/demo.robot'], stdout=subprocess.PIPE)
        
        p2.communicate()
        os.rmdir('results')

    except Exception as exc:
        print(exc)
        exitcode = 1

    finally:
        p1.terminate()
        p2.terminate()
        exit(exitcode)