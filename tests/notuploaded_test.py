import glob
import os

photopath = "../samplepics/backupcheck/"

missedfile_appendix = "-FILENOTUPLOADED"

checkstr = photopath + "*" + missedfile_appendix + "*"

print checkstr

filesnotuploaded = glob.glob(photopath + "*" + missedfile_appendix + "*")

print filesnotuploaded

if len(filesnotuploaded) > 0:

    print os.path.basename(filesnotuploaded[0])

else:
    print "none found"