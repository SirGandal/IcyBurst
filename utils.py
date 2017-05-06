from genericpath import exists
import csv
from os.path import isfile, join
import os

def getFileNameFromPath(path):
    return path.split('/')[-1]

def loadPreDefinedStatuses(PHOTO_FOLDERS):
    # for each folder we can have a csv file that contains file name and the status to use in the tweet or instagram photo
    statuses = []
    for folder in PHOTO_FOLDERS:
        folderImagesCsv = folder + ".csv"
        if exists(folderImagesCsv): 
            print "Reading pre defined statuses from " + folderImagesCsv 
            with open(folderImagesCsv, 'r') as f:
                reader = csv.reader(f)
                folderImagesText = list(reader)
                print str(len(folderImagesText)) + " statuses found in " + folder
                statuses = statuses + folderImagesText
    
    print str(len(statuses)) + " total pre defined status found."
    
    return statuses

def loadQuotesFromFiles(QUOTES_FILENAMES):
    quotes=[]
    print "Reading quotes from " + ", ".join(QUOTES_FILENAMES)
    for quoteFilePath in QUOTES_FILENAMES:
        with open(quoteFilePath, 'r') as f:
            reader = csv.reader(f)
            tmpQuotes = list(reader)
            del tmpQuotes[0] #remove csv headers
            print str(len(tmpQuotes)) + " quotes found in " + quoteFilePath
            quotes = quotes + tmpQuotes
    
    print str(len(quotes)) + " total quotes found."
    
    return quotes

def loadImagesFromFolders(PHOTO_FOLDERS):
    print "Scanning directories for images..."
    images = []
    for folder in PHOTO_FOLDERS:
        folderImages =  [join(folder, filename) for filename in os.listdir(folder) if isfile(join(folder, filename)) and not filename.startswith(".")]
        print str(len(folderImages)) + " images found in " + folder
        images = images + folderImages
        
    print str(len(images)) + " total images found."
    
    return images