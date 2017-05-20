from twython import Twython, TwythonError
from random import randint
import random
from common import *
import threading
from utils import getFileNameFromPath, loadQuotesFromFiles
import os

class TBot:
    
    TAGS = []
    MENTIONS = []
    MAX_STATUS_LENGTH = 140
    TWITTER_USED_QUOTES_FILENAME = ""
    TWITTER_USED_IMAGES_FILENAME = ""
    QUOTES_FILENAMES = []
    APP_KEY = ""
    APP_SECRET = ""
    OAUTH_TOKEN = ""
    OAUTH_TOKEN_SECRET = ""
    MAX_IMAGE_SIZE = 3145728
    twitter = None
    
    def __init__(self, APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET):
        self.APP_KEY = APP_KEY
        self.APP_SECRET = APP_SECRET
        self.OAUTH_TOKEN = OAUTH_TOKEN
        self.OAUTH_TOKEN_SECRET = OAUTH_TOKEN_SECRET
        self.twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    
    def isStatusValid(self, status):
        # note that mentions don't count for the limit
        #return  len(status) - len(" ".join(self.MENTIONS)) <= self.MAX_STATUS_LENGTH
        return  len(status) <= self.MAX_STATUS_LENGTH 
    
    def filterStatusesForCharactersLimit(self, quotes):
        print "Filtering quotes for Twitter (< 140)."
        twitterQuotes = []
        for quote in quotes:
            if TBot.isStatusValid(self, getStatusFromRandomQuote(quote, self.TAGS, self.MENTIONS)):
                twitterQuotes.append(quote)
        print str(len(twitterQuotes)) + " twitter quotes left."
        return twitterQuotes
    
    @staticmethod
    def authorizeApplicationAndInitialize(APP_KEY, APP_SECRET):
        twitter = Twython(APP_KEY, APP_SECRET)

        auth = twitter.get_authentication_tokens()
    
        OAUTH_TOKEN = auth['oauth_token']
        OAUTH_TOKEN_SECRET = auth['oauth_token_secret']
    
        twitter = Twython(APP_KEY, APP_SECRET,OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    
        print "Authorize app here: " + auth['auth_url']
    
        oauth_verifier=raw_input('Enter the PIN:')
    
        twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    
        print "Authenticating..."
    
        final_step = twitter.get_authorized_tokens(oauth_verifier)
    
        OAUTH_TOKEN = final_step['oauth_token']
        OAUTH_TOKEN_SECRET = final_step['oauth_token_secret']
        
        return TBot(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    
    def run(self, minWait, maxWait, images, quotes, preDefinedStatuses, defaultStatuses, supervised, debug):        
        n = randint(minWait, maxWait)
        print ("Twitter - Sleep upload for seconds: " + str(n))
        
        # no more images available
        if len(images) == 0:
            print "Twitter Bot terminated."
            return
        threading.Timer(n, self.run, [minWait, maxWait, images, quotes, preDefinedStatuses, defaultStatuses, supervised, debug]).start()        
        image = ""
        imageSize = self.MAX_IMAGE_SIZE + 1
        
        while imageSize > self.MAX_IMAGE_SIZE:
            if supervised:
                print "========================================================================" 
                while raw_input("Twitter - Picked image is: " + image + ". Change?") == "y":
                    image = random.choice(images)
            else:
                image = random.choice(images)
            imageSize = os.stat(image).st_size
            print str(imageSize) +  " bytes"
        
        # if we don't have a quote pre-defined for this picture let's pick a random one that
        # we don't have already used
        foundPreDefinedStatus = ""
        for preDefinedStatuse in preDefinedStatuses:
            if getFileNameFromPath(image) == preDefinedStatuse[0] and preDefinedStatuse[1] != "":
                foundPreDefinedStatus = preDefinedStatuse[1]
                status = getStatusFromText(foundPreDefinedStatus, self.TAGS, self.MENTIONS)
                continue
        
        randomQuote = []
        if foundPreDefinedStatus == "" and supervised:
            
            # if we run out of quotes, let's recycle old ones
            if len(quotes) == 0:
                os.remove(self.TWITTER_USED_QUOTES_FILENAME)
                quotes = loadQuotesFromFiles(self.QUOTES_FILENAMES)
                quotes = TBot.filterStatusesForCharactersLimit(self, quotes)
            
            # Since we scraped for quotes, some are not appropriate, ask the user if he/she wants to pick a new one
            keepLookinForQuote = True
            while keepLookinForQuote:
                status = 'a'*300
                while not self.isStatusValid(status):
                    randomQuote = random.choice(quotes)
                    status = getStatusFromRandomQuote(randomQuote, self.TAGS, self.MENTIONS)
                print "========================================================================" 
                keepLookinForQuote = raw_input("Twitter - The random quote is: " + randomQuote[0] + ". Is that okay?") != "y"
                
            with open(self.TWITTER_USED_QUOTES_FILENAME, "a+") as twitterUsedQuotes:
                twitterUsedQuotes.write(randomQuote[0]+"\n")
            #remove the used quote from the list of usable ones
            quotes.remove(randomQuote)
        else:
            if foundPreDefinedStatus == "":
                status = random.choice(defaultStatuses)
            
        with open(self.TWITTER_USED_IMAGES_FILENAME, "a+") as twitterUsedImages:
            twitterUsedImages.write(getFileNameFromPath(image)+"\n")
        #remove the used image from the list of usable ones
        images.remove(image)
            
        photo = open(image, 'rb')
        
        print ("Twitter - Progress: " + str(len(images)) + " left")
        print ("Twitter - Now Uploading photo " + getFileNameFromPath(image))
        print ("Twitter - Status " + status)
        
        tryCount = 0
        if not debug:
            
            uploadError = "Error"
            
            while uploadError != "" and tryCount <= 3:
                tryCount = tryCount + 1
                try:
                    response = self.twitter.upload_media(media=photo)
                    print response
                    uploadError = ""
                except TwythonError as e:
                    uploadError = str(e.error_code)
                    print "There was an error while trying to upload a photo. Code: " + uploadError
                    print "Trying twitter photo upload again..."
            if tryCount <= 3:
                try:
                    self.twitter.update_status(status=status, media_ids=[response['media_id']])
                except TwythonError as e:
                    print "There was an error while trying to upload a tweet. Code: " + str(e.error_code)
            
                
            
       
