import unittest
import tweepy
import requests
import json
import twitter_info

## SI 206 - HW
## COMMENT WITH:
##Robert Cole Burgess
## Your section day/time: 001 MONDAY/WEDENSEDAY  2:30-4 PM
## Any names of people you worked with on this assignment:

import sys##fixing encoding error
def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)

## Write code that uses the tweepy library to search for tweets with three different phrases of the
## user's choice (should use the Python input function), and prints out the Tweet text and the
## created_at value (note that this will be in GMT time) of the first FIVE tweets with at least
## 1 blank line in between each of them, e.g.


## You should cache all of the data from this exercise in a file, and submit the cache file
## along with your assignment.

## So, for example, if you submit your assignment files, and you have already searched for tweets
## about "rock climbing", when we run your code, the code should use CACHED data, and should not
## need to make any new request to the Twitter API.  But if, for instance, you have never
## searched for "bicycles" before you submitted your final files, then if we enter "bicycles"
## when we run your code, it _should_ make a request to the Twitter API.

## Because it is dependent on user input, there are no unit tests for this -- we will
## run your assignments in a batch to grade them!

## We've provided some starter code below, like what is in the class tweepy examples.

##SAMPLE OUTPUT
## See: https://docs.google.com/a/umich.edu/document/d/1o8CWsdO2aRT7iUz9okiCHCVgU5x_FyZkabu2l9qwkf8/edit?usp=sharing



## **** For extra credit, create another file called twitter_info.py that
## contains your consumer_key, consumer_secret, access_token, and access_token_secret,
## import that file here.  Do NOT add and commit that file to a public GitHub repository.

## **** If you choose not to do that, we strongly advise using authentication information
## for an 'extra' Twitter account you make just for this class, and not your personal
## account, because it's not ideal to share your authentication information for a real
## account that you use frequently.

## Get your secret values to authenticate to Twitter. You may replace each of these
## with variables rather than filling in the empty strings if you choose to do the secure way
## for EC points
# consumer_key = twitter_info_example.consumer_key
# consumer_secret = twitter_info_example.consumer_secret
# access_token = twitter_info_example.access_token
# access_token_secret = twitter_info_example.access_token_secret
## Set up your authentication to Twitter
consumer_key = twitter_info.consumer_key##EXTRA CREDIT AND ACCESS TO TWITTER VIA KEY AND TOKEN FILE VARIABLES
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)##AUTHORIZATION
auth.set_access_token(access_token, access_token_secret)

# Set up library to grab stuff from twitter with your authentication, and
# return it in a JSON-formatted way

api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())##API LIBRARY RETURNING AS JSON DICT
CACHE_FNAME = 'cache_already_searched.json' # String for your file. We want the JSON file type, bcause that way, we can easily get the information into a Python dictionary!

try:
    cache_file = open(CACHE_FNAME, 'r') # Try to read the data from the file
    cache_contents = cache_file.read()  # If it's there, get it into a string
    CACHE_DICTION = json.loads(cache_contents) # And then load it into a dictionary
    cache_file.close() # Close the file, we're good, we got the data in a dictionary.
except:
    CACHE_DICTION = {}

## Write the rest of your code here!
#### Recommended order of tasks: ####
## 1. Set up the caching pattern start -- the dictionary and the try/except
## 		statement shown in class.
def Twittersearch(words):
    if words in CACHE_DICTION:##IF SEARCH TERM IN CACHE TELL USER
        print("Data was in the cache")
        return CACHE_DICTION[words]
    else:
        print("getting data")##IF NEEDED TO BE SEARCHED TELL USER, SEARCH API, AND WRITE TO THE CACHE FILE
        results=api.search(q=words)
        CACHE_DICTION[words]=results
        cache_file=open(CACHE_FNAME, 'w')
        cache_file.write(json.dumps(CACHE_DICTION))
        cache_file.close()##CLOSE FILE TO ENSURE NO OVERLOAD
    return results
for i in range(3):##ONLY SEARCH THREE INPUTS GIVEN
    mywords=input('enter twitter term:')
    search_result=Twittersearch(mywords)
    for r in search_result["statuses"][:5]:##RETURN FIRST FIVE RESULTS
        uprint("text:", r["text"])##TEXT OF TWEETS
        uprint("created_at:",r['created_at'])##TIME CREATED
        uprint("\n")
uprint("done")



## 2. Write a function to get twitter data that works with the caching pattern,
## 		so it either gets new data or caches data, depending upon what the input
##		to search for is.



## 3. Using a loop, invoke your function, save the return value in a variable, and explore the
##		data you got back!


## 4. With what you learn from the data -- e.g. how exactly to find the
##		text of each tweet in the big nested structure -- write code to print out
## 		content from 5 tweets, as shown in the linked example.
