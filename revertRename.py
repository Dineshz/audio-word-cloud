from os import listdir, path, rename

EXTENSION = ".processed"

fileList = listdir("./")
fileList = [ fileName for fileName in fileList if path.splitext(fileName)[1] == EXTENSION]
for fileName in fileList:
  rename(fileName, fileName.replace(EXTENSION, ''))