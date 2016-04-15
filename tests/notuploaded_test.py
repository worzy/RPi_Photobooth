import glob
import os

photopath = "../samplepics/backupcheck/"

missedfile_appendix = "-FILENOTUPLOADED"

checkstr = photopath + "*" + missedfile_appendix + "*"

print checkstr

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
    else:
        print "somethings fucked"
else:
    print "none found"