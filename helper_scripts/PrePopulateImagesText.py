import os
from os.path import isfile, join, isdir
import csv
import sys

def getFileName(uri):
    return uri.split('/')[-1]

photoFolderName = raw_input('Enter relative path to the folder containg photos:').strip()
if not os.path.isdir(photoFolderName):
	print "Folder (" + photoFolderName + ") doesn't exist."
	sys.exit()
	
print "Scanning directory for images..."
images = [join(photoFolderName, filename) for filename in os.listdir(photoFolderName) if isfile(join(photoFolderName, filename)) and not filename.startswith(".")]
print str(len(images)) + " images found."

with open(photoFolderName + '.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    for image in images:
        writer.writerow([getFileName(image), ""])
        
