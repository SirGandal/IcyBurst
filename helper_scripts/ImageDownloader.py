import urllib
import csv
import os
import time
from random import randint
from genericpath import exists

BASE_FILE_NAME = raw_input('Enter the base filename of the CSV file (If you enter FILENAME the script will try to load FILENAME (0).csv and so on with incremental numbers):').strip()
DOWNLOAD_PATH = raw_input('Enter images relative download destination:').strip()

if exists(DOWNLOAD_PATH):
	print "Images destination (" + DOWNLOAD_PATH + ") doesn't exist"

fileIndex = 0

while True:
    fileName = BASE_FILE_NAME + " (" + str(fileIndex) +").csv"
    
    if not os.path.isfile(fileName):
        print fileName + " does not exist. Ending downloads."
        break
    
    with open(fileName, 'r') as f:
        reader = csv.reader(f)
        items = list(reader)

    for i in range(1, len(items)):
        downloadUrl = items[i][0]
        downloadFileName = downloadUrl.split('/')[-1]
        if exists(DOWNLOAD_PATH + downloadFileName): 
            print "skipping " + downloadFileName
            continue
        print "downloading: " + downloadFileName
        urllib.urlretrieve(downloadUrl, DOWNLOAD_PATH + downloadFileName)
        
        # let's wait between 35 and 75 seconds so that it doesn't arouse suspicion
        sleepFor=randint(35, 75)
        print "sleep for " + str(sleepFor) + " seconds"
        time.sleep(sleepFor)
        
    fileIndex = fileIndex + 1
