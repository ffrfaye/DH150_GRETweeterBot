# botfaye.py
# Rufei Fan
# UID: 304-456-532
# A GRE word bot: Midterm project for DH 150. Tweets random GRE words and definitions.

import tweepy
import csv
import time
import random
import sys



############### SETUPS ###############################

# Consumer keys and access tokens, used for OAuth
consumer_key = 'PtgpThubWYNiof47P1RsUTWWN'
consumer_secret = 's5WGxsgrXCrXcvFi7stfIHUV9UNYrSvOyELbT5vpOJ2fR7lJEa'
access_token = '3128883672-S25Oxn2LY1LcSjHoy4zbBhZYpylXHkFi3cOU9Rn'
access_token_secret = '03Y1e5Pm6gMZZaDkjiit4Coliz0UuzPHGkPBNzHrhdyOZ'

# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Creation of the actual interface, using authentication
api = tweepy.API(auth)
robotName = 'bot faye'

# Get the api for a particular user
user = api.me()

# Fix for an encoding error. Basically Twitter allows characters that IDLE can't print out, so
# you have to remove the characters that lie outside of this range.
#
# Whenever you want to print text, use .translate(non_bmp_map) on the end.
# e.g. str(myVar).translate(non_bmp_map)
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

# A dictionary storing old tweets that have been replied to
old_twts = {}



############### FUNCTIONS ###############################

# Function 1: open CSV file and generate a dictionary.

def csv_to_dict(filename):
    infile = open(filename)
    reader = csv.reader(infile)
    data = list(reader)

    to_return = {}
    for row in data:
        to_return[row[0]] = row[1]

    return to_return

# Function 2: distinguish whether a tweet is new and need to be replied

def if_twt_need_reply(twtid):
    if twtid in old_twts:
        return False
    else:
        old_twts[twtid] = 1
        return True


# Function 3: reply to new tweets that are tweeted at me

def reply_twt():
    # Search for tweets tweeted at me
    twt_to_me = api.search(q='@' + str(user.screen_name), count=10)

    # Loop through the results and evaluate whether the tweets need to be replied
    for i in twt_to_me:
        if i.user.screen_name != user.screen_name:
            if if_twt_need_reply(str(i.id)):
                name = str(i.user.screen_name).translate(non_bmp_map)
                to_tweet = 'ty @' + name + ' for trying to interact with me but im just an emotionless bot hehe'
                api.update_status(to_tweet)






############### START THE LOOP ####################

word_dict = csv_to_dict('vocabulary.csv')

while bool(word_dict):

    # check tweets tweeted at me, and reply if necessary
    reply_twt()

    # 15% chance send out a tweet
    seed = random.randint(100, 500)
    if seed % 7 == 0:

        # use popitem so that every tweet will be unique and deleted from the dict when it's tweeted
        word_to_tweet = word_dict.popitem()

        api.update_status(word_to_tweet[0] + " : " + word_to_tweet[1] + " #DH150 #StudyUrGREWordsYay")
        time.sleep(300)

