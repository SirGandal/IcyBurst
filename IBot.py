from InstagramAPIpython.InstagramAPI import InstagramAPI
from random import randint
from common import getStatusFromRandomQuote, getStatusFromText
import threading
from utils import getFileNameFromPath
from shutil import copyfile
import time

class IBot:
    TAGS = []
    MENTIONS = []
    INSTAGRAM_USED_QUOTES_FILENAME = ""
    INSTAGRAM_USED_IMAGES_FILENAME = ""
    GOOGLE_DRIVE_PATH = ""
    username = ""
    password = ""
    
    igapi = None
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.igapi = InstagramAPI(username,password)
        #self.igapi.login()
    
    def run(self, minWait, maxWait, images, quotes, preDefinedStatuses, debug):
        n = randint(minWait, maxWait)
        print ("Instagram - Sleep upload for seconds: " + str(n))
        
        # no more images available
        if len(images) == 0:
            print "Instagram Bot terminated."
            return
        threading.Timer(n, self.run, [minWait, maxWait, images, quotes, preDefinedStatuses, debug]).start()
        
        image = ""
        print "========================================================================" 
        while raw_input("Instagram - Picked image is: " + image + ". Change?") == "y":
            image = images[randint(0, len(images))]
            
        # if we don't have a quote pre-defined for this picture let's pick a random one that
        # we don't have already used
        foundPreDefinedStatus = ""
        for preDefinedStatuse in preDefinedStatuses:
            if getFileNameFromPath(image) == preDefinedStatuse[0] and preDefinedStatuse[1] != "":
                foundPreDefinedStatus = preDefinedStatuse[1]
                status = getStatusFromText(foundPreDefinedStatus, self.TAGS, self.MENTIONS)
                continue
        
        randomQuote = []
        if foundPreDefinedStatus == "":
            
            # Since we scraped for quotes, some are not appropriate, ask the user if he/she wants to pick a new one
            keepLookinForQuote = True
            while keepLookinForQuote:
                quoteIndex = randint(0, len(quotes)+1)
                randomQuote = quotes[quoteIndex]
                status = getStatusFromRandomQuote(randomQuote, self.TAGS, self.MENTIONS)
                
                print "========================================================================" 
                keepLookinForQuote = raw_input("Instagram - The random quote is: " + randomQuote[0] + ". Is that okay?") != "y"
            
            with open(self.INSTAGRAM_USED_QUOTES_FILENAME, "a+") as instagramUsedQuotes:
                instagramUsedQuotes.write(randomQuote[0]+"\n")
                
            #remove the used quote from the list of usable ones
            quotes.remove(randomQuote)
        
        with open(self.INSTAGRAM_USED_IMAGES_FILENAME, "a+") as instagramUsedImages:
            instagramUsedImages.write(getFileNameFromPath(image)+"\n")
        #remove the used image from the list of usable ones
        images.remove(image)
            
        photo = open(image, 'rb')
        
        print ("Instagram - Progress: " + str(len(images)) + " left")
        print ("Instagram - Now Uploading photo " + image + " and status " + status)
        
        if not debug:
            # Sometimes it happens that the instagram upload photo fails
            # as a consequence we move the photo to a drive folder so that
            # we can later upload it manually from the phone app
            copyfile(image, self.GOOGLE_DRIVE_PATH + getFileNameFromPath(image))
            with open(self.GOOGLE_DRIVE_PATH + getFileNameFromPath(image)+".txt", "a+") as statusForImageFile:
                statusForImageFile.write(status)
            
            self.igapi.login(True);
            time.sleep(randint(60, 90))
            self.igapi.uploadPhoto(image,caption=status,upload_id=None)
            time.sleep(randint(20, 45))
            self.igapi.logout()
