import glob

photopath = "../samplepics/backupcheck/"

missedfile_appendix = "FILENOTUPLOADED"

filesnotuploaded = glob.glob(photopath + "*" + missedfile_appendix + "*")

print filesnotuploaded