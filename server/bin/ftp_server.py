from optparse import OptionParser
import os
import sys
import SocketServer
BASE_DIR = os.path.dirname(os.path.dirname( os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from module import thread_server
from conf import settings

def main():
    usage = "usage: %prog start/stop "
    parser = OptionParser(usage)
    (options, args) = parser.parse_args()
    if len(args) !=  1:
        sys.exit(usage)

    if args[0] != 'start' and args[0] != 'stop':
        sys.exit(usage)

    if hasattr(__import__(__name__),args[0]):
        func = getattr(__import__(__name__),args[0])
        func()


def start():
    try:
        server = SocketServer.ThreadingTCPServer((settings.BIND_HOST, settings.BIND_PORT), thread_server.FtpServer)
        server.serve_forever()
    except KeyboardInterrupt:
        print("----going to shutdown ftp server-----")
        server.shutdown()



if __name__ == "__main__":
    main()