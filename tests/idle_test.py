import time
import socket

idle_time = 1
test_server = "www.google.com"


def is_connected():
    try:
        # see if we can resolve the host name -- tells us if there is
        # a DNS listening
        host = socket.gethostbyname(test_server)
        # connect to the host -- tells us if the host is actually
        # reachable
        s = socket.create_connection((host, 80), 2)
        return True
    except:
        pass
    return False


def idle_stuff():
    connected = is_connected()

    if connected:
        print "uploading missing files"
    else:
        print "not connected :("




tstart = time.time()

try:
    while True:
        tcurrent = time.time()

        if (tcurrent - tstart) > idle_time:
            print "do idle stuff"
            idle_stuff()
            tstart = tcurrent

except KeyboardInterrupt:
    print "stopping now"