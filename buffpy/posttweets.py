#!/usr/bin/env python
# encoding: utf-8
 
from buffpy import API
from buffpy import AuthService
from buffpy.managers.profiles import Profiles
from buffpy.managers.updates import Updates
from buffpy.models.update import Update
from buffpy.models.user import User
 
from colorama import Fore
from cStringIO import StringIO
 
import itertools
import unicodecsv
import json
 
client_id = '53d83f40a3f4209d1d524542'
client_secret = 'df48fe7f68b2bb11384a8460016ba18d'
 
redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'
 
service = AuthService(client_id, client_secret, redirect_uri)
 
url = service.authorize_url
 
print 'Access this url and retrieve the token: \n' + Fore.YELLOW + 'Command + Double Click: ' + Fore.BLUE + url + Fore.RESET
 
auth_code = raw_input('Paste the code from the redirected url: ')
access_token = service.get_access_token(auth_code)
print 'Access TOKEN: ' + access_token
 
api = service.create_session(access_token)
 
# instantiate the api object
api = API(client_id='client_id',
          client_secret='client_secret',
          access_token=access_token)
 
# filter profiles using some criteria
profile = Profiles(api=api).filter(service='twitter')[0]
 
tweets_file = '../tweepy/nicosuave/tweets.csv'
 
start = input("From tweet #: ")
stop = input("To tweet #: ")
 
# create a buffer tweet
with open(tweets_file, 'rb') as csvfile:
  tweetreader = unicodecsv.reader(csvfile, encoding='ascii')
 
  # post each row to buffer 
  for row in itertools.islice(tweetreader, start-1, stop):
 
    # variable to hold the tweet's text
    buffer_tweet = ''.join(row[0])
 
    # parse out the unwanted hyperlink
    if "http://t.co/" in buffer_tweet:
      buffer_tweet = buffer_tweet[:-22]
 
    # print on terminal
    print buffer_tweet
 
    # variable to hold the tweet's media in list format
    buffer_media = json.loads(row[1])
 
    #print buffer_media
 
    # if the list isn't empty transform it to JSON
    if buffer_media != None:
       
      media_dict = {}
 
      for di in buffer_media:
        media_dict[di['id']] = {}
 
      for k in di.keys():
        if k =='id': 
          continue
        media_dict[di['id']][k]=di[k]
 
      # save the media_url_https
      media_json = media_dict.get(di['id'])
      media_link = media_dict.get(di['id']).get('media_url').encode('utf-8')
      media_thumb = media_dict.get(di['id']).get('media_url').encode('utf-8')
      new_update_media = {
        "picture": media_link,
        "thumbnail": media_thumb
      }
      print new_update_media
 
    # post to buffer with current schedule
    if buffer_media == None:
      profile.updates.new(buffer_tweet, now=False, media=None)
    else:
      profile.updates.new(buffer_tweet, now=False, media=new_update_media)