# Import statements
import unittest
import sqlite3
import requests
import json
import re
import tweepy
import twitter_info  # still need this in the same directory, filled out

print('welcome')##let user know running
import sys##fixing encoding error
def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)

consumer_key = twitter_info.consumer_key  ## take access info/keys/tokens from file twitter_info
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Set up library to grab stuff from twitter with your authentication, and return it in a JSON format
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

# And we've provided the setup for your cache. But we haven't written any functions for you, so you have to be sure that any function that gets data from the internet relies on caching.
cache_fname = 'twitterfile.json' # String for your file. We want the JSON file type, bcause that way, we can easily get the information into a Python dictionary!

try:
    cache_file = open(cache_fname, 'r') # Try to read the data from the file
    cache_contents = cache_file.read()  # If it's there, get it into a string
    cache_contents.close() # Close the file, we're good, we got the data in a dictionary
    cache_diction= json.loads(cache_contents) # And then load it into a dictionary
except:
    cache_diction = {}##if not in the file still create empty dict to insert cache or tweet scrape

## [PART 1]

# Here, define a function called get_tweets that searches for all tweets referring to or by "umsi"
# Your function must cache data it retrieves and rely on a cache file!


def get_tweets():
##YOUR CODE HERE
    cache_diction={}
    tweets='umsi'##give keyword a variable
    if tweets in cache_diction:##if search word is in cache go no further
        print('using cached data')##let user know using cache
        twitter_results=cache_diction[tweets]
    else:
        print('getting data from the internet')##let user know not in cache/scraping
        twitter_results=api.user_timeline(tweets)##if tweet not in cache already scrape twitter
        cache_diction[tweets]=twitter_results
        f=open(cache_fname,'w')##open file internet option to cache
        f.write(json.dumps(cache_diction))##write scrape to cache for json
        f.close()##close file
        print(type(twitter_results))##for my sanity


    return twitter_results##return cache and/or internet tweet and info
## [PART 2]
# Create a database: tweets.sqlite,
# And then load all of those tweets you got from Twitter into a database table called Tweets, with the following columns in each row:
## tweet_id - containing the unique id that belongs to each tweet
## author - containing the screen name of the user who posted the tweet (note that even for RT'd tweets, it will be the person whose timeline it is)
## time_posted - containing the date/time value that represents when the tweet was posted (note that this should be a TIMESTAMP column data type!)
## tweet_text - containing the text that goes with that tweet
## retweets - containing the number that represents how many times the tweet has been retweeted

# Below we have provided interim outline suggestions for what to do, sequentially, in comments.

# 1 - Make a connection to a new database tweets.sqlite, and create a variable to hold the database cursor.
print('tests for part 2')

conn=sqlite3.connect('tweets.sqlite')##connect to my database
cur = conn.cursor()##cursor variable cur
print('tests for part 2') # let user know new tests
    # 2 - Write code to drop the Tweets table if it exists, and create the table (so you can run the program over and over), with the correct (4) column names and appropriate types for each.
# HINT: Remember that the time_posted column should be the TIMESTAMP data type!
cur.execute('DROP TABLE IF EXISTS tweets')##refresh tables if already exists drop
cur.execute('CREATE TABLE Tweets(tweet_id TEXT, author TEXT, time_posted TIMESTAMP, tweet_text TEXT, retweets NUMBER)')##create fresh table with desired info


# 3 - Invoke the function you defined above to get a list that represents a bunch of tweets from the UMSI timeline. Save those tweets in a variable called umsi_tweet
umsi_tweet=get_tweets()##invoke function loop
# 4 - Use a for loop, the cursor you defined above to execute INSERT statements, that insert the data from each of the tweets in umsi_tweets into the correct columns in each row of the Tweets database table.

for tw in umsi_tweet:
    tup=tw['id'], tw['user']['screen_name'], tw['created_at'], tw['text'], tw['retweet_count']##create table with for loop for formatting
    cur.execute('INSERT INTO Tweets (tweet_id, author, time_posted, tweet_text, retweets) VALUES (?,?,?,?,?)', tup)
#  5- Use the database connection to commit the changes to the database
    conn.commit()##commit my changes
# You can check out whether it worked in the SQLite browser! (And with the tests.)

## [PART 3] - SQL statements
# Select all of the tweets (the full rows/tuples of information) from umsi_tweets and display the date and message of each tweet in the form:
    # Mon Oct 09 16:02:03 +0000 2017 - #MondayMotivation https://t.co/vLbZpH390b
    #
    # Mon Oct 09 15:45:45 +0000 2017 - RT @MikeRothCom: Beautiful morning at @UMich - It’s easy to forget to
    # take in the view while running from place to place @umichDLHS  @umich…
# Include the blank line between each tw
# Select the author of all of the tweets (the full rows/tuples of information) that have been retweeted MORE
# than 2 times, and fetch them into the variable more_than_2_rts. nnnn
# Print the results
cur.execute('SELECT time_posted,tweet_text FROM Tweets')#cursor selects timstamp for retweets
alltweetsauthor=cur.fetchall()##finds authors
for t in alltweetsauthor:
    uprint(t[0]+"-"+t[1]+'\n')##selects table elements to print before retweets
    more_than_2_rts=cur.execute('SELECT author FROM Tweets WHERE retweets>2')##finds retweets over 2
    uprint(more_than_2_rts)##prints retweets over 2
cur.close()


if __name__ == "__main__":
    unittest.main(verbosity=2)
