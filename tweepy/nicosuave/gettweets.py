#!/usr/bin/env python
# encoding: utf-8
 
import tweepy
import codecs
import unicodecsv
import json
 
# Go to http://dev.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key="04WM70twqUuVPkWphp9Vk5cqm"
consumer_secret="kMi86B6UL71EVtPtzmhtQM1uv4pnTW5xbA4Ianegd5hu3vpURY"
 
# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token="33284712-28XiaMZEhNcGYPcEpaxKEAlRdd5nB1zlj6UeqNfk5"
access_token_secret="MPqmKIGmFnXgH8bu1Kw3tNzlOOt0uUAQzn1sEf4tKsTEq"
 
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
 
api = tweepy.API(auth)
 
def get_all_tweets(screen_name):
    #Twitter only allows access to a users most recent 3240 tweets with this method
 
    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
 
    #initialize a list to hold all the tweepy Tweets
    alltweets = []
 
    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name, count=200, include_rts=False)
 
    #save most recent tweets
    alltweets.extend(new_tweets)
 
    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
 
    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
 
        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name, count=200, max_id=oldest, include_rts=False)
 
        #save most recent tweets
        alltweets.extend(new_tweets)
 
        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
 
        #print "...%s tweets downloaded so far" % (len(alltweets))
 
    #transform the tweepy tweets into an array that will populate the csv
    outtweets = [[tweet.text.encode('ascii', 'ignore'), json.dumps(tweet.entities.get('media'))] for tweet in alltweets]
 
    # write the csv
    with codecs.open('tweets.csv', 'wb') as f:
        writer = unicodecsv.writer(f)
        writer.writerows(outtweets)
    pass
 
if __name__ == '__main__':
    username = raw_input("Twitter account to pull tweets from: ")
    #pass in the username of the account you want to download
    get_all_tweets(username)