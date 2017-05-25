import json
import csv
import os
from os.path import isfile, join

#===============================================================================
# If NeedDownloadError('Need ffmpeg exe. ' NeedDownloadError: Need ffmpeg exe)
# uncomment the following lines and run the code again
# import imageio
# imageio.plugins.ffmpeg.download()
#===============================================================================

from TBot import TBot
from IBot import IBot
from common import *
from genericpath import exists
from utils import loadPreDefinedStatuses, loadQuotesFromFiles, loadImagesFromFolders
import sys

# Load configuration from file
with open("config.json") as configJson:
    config = json.load(configJson)
    
    DEBUG_MODE = config["debug"]
    SECRETS_JSON = config["secretsPath"]
    PHOTO_FOLDERS = config["photoFoldersPath"]
    QUOTES_FILENAMES = config["quotesFoldersPath"]
    GOOGLE_DRIVE_PATH = config["googleDriveInstagramFolderPath"]
    # supervised refers to a state where the user is at the computer
    # and can decide if a photo with a given quote should be uploaded or not
    TWITTER_SUPERVISED = config["twitter"]["supervised"]
    TWITTER_ENABLED = config["twitter"]["enabled"]
    TWITTER_USED_QUOTES_FILENAME = config["twitter"]["usedQuotesFilename"]
    TWITTER_USED_IMAGES_FILENAME = config["twitter"]["usedImagesFilename"]
    TWITTER_DEFAULT_STATUSES = config["twitter"]["defaultStatuses"]
    TWITTER_TAGS = config["twitter"]["tags"]
    TWITTER_MENTIONS = config["twitter"]["mentions"]
    INSTAGRAM_ENABLED = config["instagram"]["enabled"]
    INSTAGRAM_SUPERVISED = config["instagram"]["supervised"]
    INSTAGRAM_USED_QUOTES_FILENAME = config["instagram"]["usedQuotesFilename"]
    INSTAGRAM_USED_IMAGES_FILENAME = config["instagram"]["usedImagesFilename"]
    INSTAGRAM_DEFAULT_STATUSES = config["instagram"]["defaultStatuses"]
    INSTAGRAM_TAGS = config["instagram"]["tags"]
    INSTAGRAM_MENTIONS = config["instagram"]["mentions"]
    UPLOAD_MIN_WAIT = config["minWait"]
    UPLOAD_MAX_WAIT = config["maxWait"]
    
    print "debug" + " " + str(config["debug"])
    print "secretsPath" + " " + config["secretsPath"] 
    print "photoFoldersPath" + " " + str(config["photoFoldersPath"])
    print "quotesFoldersPath" + " " + str(config["quotesFoldersPath"])
    print "googleDriveInstagramFolderPath" + " " + str(config["googleDriveInstagramFolderPath"])
    print "minWait" + " " + str(config["minWait"])
    print "maxWait" + " " + str(config["maxWait"])
    print "twitter usedQuotesFilename" + " " + str(config["twitter"]["supervised"])
    print "twitter usedQuotesFilename" + " " + str(config["twitter"]["usedQuotesFilename"])
    print "twitter usedImagesFilename" + " " + str(config["twitter"]["usedImagesFilename"])
    print "twitter tags" + " " + str(config["twitter"]["tags"])
    print "twitter mentions" + " " + str(config["twitter"]["mentions"])
    print "instagram usedQuotesFilename" + " " + str(config["instagram"]["supervised"])
    print "instagram usedQuotesFilename" + " " + str(config["instagram"]["usedQuotesFilename"])
    print "instagram usedImagesFilename" + " " + str(config["instagram"]["usedImagesFilename"])
    print "instagram tags" + " " + str(config["instagram"]["tags"])
    print "instagram mentions" + " " + str(config["instagram"]["mentions"])

twitter_APP_KEY = ""
twitter_APP_SECRET = ""
twitter_OAUTH_TOKEN = ""
twitter_OAUTH_TOKEN_SECRET = ""
instagram_username = ""
instagram_password = ""

twitterBot = None
instagramBot = None

print "Loading secrets..."

with open(SECRETS_JSON) as secretsJson:
    secrets = json.load(secretsJson)

twitterSecrets = secrets["twitter"]
instagramSecrets = secrets["instagram"]

if "APP_KEY" in twitterSecrets:
    print "Found Twitter APP_KEY"
    twitter_APP_KEY= secrets["twitter"]["APP_KEY"]
if "APP_SECRET" in twitterSecrets:
    print "Found Twitter APP_SECRET"
    twitter_APP_SECRET = secrets["twitter"]["APP_SECRET"]
if "OAUTH_TOKEN" in twitterSecrets:
    print "Found Twitter OAUTH_TOKEN"
    twitter_OAUTH_TOKEN = secrets["twitter"]["OAUTH_TOKEN"]
if "OAUTH_TOKEN_SECRET" in twitterSecrets:
    print "Found Twitter OAUTH_TOKEN_SECRET"
    twitter_OAUTH_TOKEN_SECRET = secrets["twitter"]["OAUTH_TOKEN_SECRET"]
    
if "username" in instagramSecrets:
    print "Found Instagram username"
    instagram_username = secrets["instagram"]["username"]
if "password" in instagramSecrets:
    print "Found Instagram password"
    instagram_password = secrets["instagram"]["password"]

if twitter_OAUTH_TOKEN == "" or twitter_OAUTH_TOKEN_SECRET == "":
    print "OAUTH credentials missing. Authenticating Twitter Bot..."
    twitterBot = TBot.authorizeApplicationAndInitialize(twitter_APP_KEY, twitter_APP_SECRET)

    print "Storing AUTH info for later use"
    secrets["twitter"]["OAUTH_TOKEN"] = twitterBot.OAUTH_TOKEN
    secrets["twitter"]["OAUTH_TOKEN_SECRET"] = twitterBot.OAUTH_TOKEN_SECRET
    with open(SECRETS_JSON, "w") as jsonFile:
        json.dump(secrets, jsonFile)
else:
    print "Initializing Twitter Bot..."
    twitterBot = TBot(twitter_APP_KEY, twitter_APP_SECRET, twitter_OAUTH_TOKEN, twitter_OAUTH_TOKEN_SECRET)

if INSTAGRAM_ENABLED:
    if instagram_username != "" and instagram_password != "":
        print "Initializing Instagram Bot..."
        instagramBot = IBot(instagram_username, instagram_password)
    else:
        print "Couldn't initialize Instagram Bot. Username or Password missing from " + SECRETS_JSON

images = loadImagesFromFolders(PHOTO_FOLDERS)

quotes = loadQuotesFromFiles(QUOTES_FILENAMES)

twitterQuotes = TBot.filterStatusesForCharactersLimit(twitterBot, quotes)

preDefinedStatuses = loadPreDefinedStatuses(PHOTO_FOLDERS)

print "Checking that pre defined statuses are suitable for twitter (< 140)..."
for imageText in preDefinedStatuses:
    if not TBot.isStatusValid(twitterBot, getStatusFromText(imageText[1], TBot.MENTIONS, TBot.TAGS)):
        print imageText[1] + " too long!"
 
if twitterBot is not None and TWITTER_ENABLED:
    # set file locations for writing used stuff
    twitterBot.TWITTER_USED_IMAGES_FILENAME = TWITTER_USED_IMAGES_FILENAME
    twitterBot.TWITTER_USED_QUOTES_FILENAME = TWITTER_USED_QUOTES_FILENAME
    twitterBot.TAGS = TWITTER_TAGS
    twitterBot.MENTIONS = TWITTER_MENTIONS
    twitterBot.QUOTES_FILENAMES = QUOTES_FILENAMES
    
    twitterQuotes = removeUsedQuotes(twitterQuotes, TWITTER_USED_QUOTES_FILENAME)
        
    twitterImages = removeUsedImages(images, TWITTER_USED_IMAGES_FILENAME)
    
    if len(twitterImages) > 0:
        twitterBot.run(UPLOAD_MIN_WAIT, UPLOAD_MAX_WAIT, list(twitterImages), list(twitterQuotes), list(preDefinedStatuses), list(TWITTER_DEFAULT_STATUSES), TWITTER_SUPERVISED, DEBUG_MODE)

if instagramBot is not None and INSTAGRAM_ENABLED:    
    # set file locations for writing used stuff
    instagramBot.INSTAGRAM_USED_IMAGES_FILENAME = INSTAGRAM_USED_IMAGES_FILENAME
    instagramBot.INSTAGRAM_USED_QUOTES_FILENAME = INSTAGRAM_USED_QUOTES_FILENAME
    instagramBot.GOOGLE_DRIVE_PATH = GOOGLE_DRIVE_PATH
    instagramBot.TAGS = INSTAGRAM_TAGS
    instagramBot.MENTIONS = INSTAGRAM_MENTIONS
    
    instagramQuotes = removeUsedQuotes(quotes, INSTAGRAM_USED_QUOTES_FILENAME)
    
    instagramImages = removeUsedImages(images, INSTAGRAM_USED_IMAGES_FILENAME)
    
    if len(images) > 0:
        instagramBot.run(UPLOAD_MIN_WAIT, UPLOAD_MAX_WAIT, list(instagramImages), list(instagramQuotes), list(preDefinedStatuses), list(INSTAGRAM_DEFAULT_STATUSES), TWITTER_SUPERVISED, DEBUG_MODE)



