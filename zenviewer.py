# Branch - WebZenViewer DEVELOP
import time, sys, os
from daemon3x import Daemon
from app import app
from config import basedir

class MyDaemon(Daemon):
    def run(self):
        app.run(host='localhost', port=3729, debug=True, use_reloader=False)


if __name__ == '__main__':
    # app.run(host='localhost', port=3729, debug=True)

    daemon = MyDaemon(f'{basedir}/daemon-zenviewer.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            print('Запущено на 127.0.0.1:3729\nКоманда перезапуска: python3 zenviewer.py restart\nКоманда остановки: python3 zenviewer.py stop\nКоманда проверки: python3 zenviewer.py status')
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        elif 'status' == sys.argv[1]:
            daemon.status()
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)