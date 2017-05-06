from genericpath import exists
from utils import getFileNameFromPath

def getStatusFromRandomQuote(randomQuote, tags, mentions):
        return "\"" + randomQuote[0] + "\" - " + randomQuote[1] + " " + " ".join(tags) + " " + " ".join(mentions)
    
def getStatusFromText(text, tags, mentions):
    return text + " " + " ".join(tags) + " " + " ".join(mentions)

def removeUsedImages(images, USED_IMAGES_FILENAME):
    if exists(USED_IMAGES_FILENAME):
        print "Loading used images from " + USED_IMAGES_FILENAME + " ..."
        with open(USED_IMAGES_FILENAME) as usedImagesFile:
            usedImages = usedImagesFile.readlines()
            usedImages = [img.strip() for img in usedImages] 
            print str(len(usedImages)) + " used images found."
        
        #remove used images from the list of images to upload
        if usedImages:
            images = [img for img in images if(getFileNameFromPath(img) not in usedImages)]
        
        print str(len(images)) + " images to upload."
    else:
        print USED_IMAGES_FILENAME + " does not exist."
        
    return images
    
def removeUsedQuotes(quotes, USED_QUOTES_FILENAME):
    if exists(USED_QUOTES_FILENAME):
        print "Loading used quotes from " + USED_QUOTES_FILENAME + " ..."
        with open(USED_QUOTES_FILENAME) as usedQuotesFile:
            usedQuotes = usedQuotesFile.readlines()
            usedQuotes = [quote.strip() for quote in usedQuotes] 
            print str(len(usedQuotes)) + " used quotes found."
        
        #removing used quotes from the list of usable quotes
        if usedQuotes:
            quotes = [quote for quote in quotes if(quote[0] not in usedQuotes)]
            
        print str(len(quotes)) + " quotes to use."
    else:
        print USED_QUOTES_FILENAME + " does not exist."
    
    return quotes