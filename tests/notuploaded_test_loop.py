import glob
import os
import socket
import time
import random
photopath = "../samplepics/backupcheck/"

missedfile_appendix = "-FILENOTUPLOADED"

make_tests = 1 # toggle if you want to make the test files first


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
    connected = True

    if connected:
        print "uploading missing files"
        upload_single_missingfile()
    else:
        print "not connected :("


def upload_single_missingfile():
    checkstr = photopath + "*" + missedfile_appendix + "*"
    #print "Checking with string :" + checkstr
    filesnotuploaded = glob.glob(photopath + "*" + missedfile_appendix + "*")
    print "found following files : "
    print filesnotuploaded
    numfound = len(filesnotuploaded)
    print "numfound : " + str(numfound)
    if numfound > 0:
        targetint = random.randint(0,numfound-1)
        print "targentint : " + str(targetint)
        target_name = os.path.basename(filesnotuploaded[targetint])
        print "current file :" + target_name
        name_split = str.split(target_name, missedfile_appendix)
        filetoupload = name_split[0]
        if os.path.exists(photopath + filetoupload + ".gif"):
            print "uploading with file " + filetoupload
            print "backing up too"
            print "now i can delete it too"
            os.remove(photopath + target_name)
        else:
            print "couldnt find gif deleting backupflag"
            os.remove(photopath + target_name)
    else:
        print "no missing uploads found"

# make file notuploaded
if make_tests:
    for fname in ["test", "hedgehog", "hedgehog2", "not_exist"]:
        file = open(photopath + fname + missedfile_appendix, 'w')  # Trying to create a new file or open one
        file.close()


tstart = time.time()

try:
    while True:
        tcurrent = time.time()

        if (tcurrent - tstart) > idle_time:
            print "do idle stuff"
            idle_stuff()
            tstart = tcurrent
        else:
            time.sleep(.1)

except KeyboardInterrupt:
    print "stopping now"
