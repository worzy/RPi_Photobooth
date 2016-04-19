import glob
import os

photopath = "../samplepics/backupcheck/"

missedfile_appendix = "-FILENOTUPLOADED"

checkstr = photopath + "*" + missedfile_appendix + "*"

make_tests = 0 # toggle if you want to make the test files first


print checkstr



# make file notuploaded
if make_tests:
    for fname in ["test", "hedgehog", "hedgehog2"]:
        file = open(photopath + fname + missedfile_appendix, 'w')  # Trying to create a new file or open one
        file.close()


filesnotuploaded = glob.glob(photopath + "*" + missedfile_appendix + "*")

print filesnotuploaded

if len(filesnotuploaded) > 0:

    target_name = os.path.basename(filesnotuploaded[0])
    print target_name
    name_split = str.split(target_name,missedfile_appendix)
    filetoupload = name_split[0]
    if os.path.exists(photopath + filetoupload + ".gif"):
        print "uploading with file " + filetoupload
        print "backing up too"
        print "now i can delete it too"
        os.remove(photopath + target_name)
    else:
        print "somethings fucked"
else:
    print "none found"