# -*- coding: UTF-8 -*-
import sys
import os
import inspect
import time
import json
import tweepy
import csv
import logging

import config as cfg
from datetime import datetime, timedelta
from pytz import timezone
from tweepy.error import TweepError
from tweepy.parsers import JSONParser
from db import insert_tweet_data

def read_input(inp):
    try:
        incsvfile = open(inp, 'r')
        infile = csv.DictReader(incsvfile)
        tweet_id = []
        for row in infile:
            tweet_id.append(row['tweet_id'].replace('ID_', ''))
        return tweet_id
    except Exception as e:
        print("Error occurred [{}]. Try again.".format(e))
        sys.exit(-1)
            
def run_insert(filename):
    with open(filename, 'r') as infile:
        lines = infile.readlines()
        for line in lines:
            try:
                insert_tweet_data(json.loads(line))
            except Exception as e:
                template = "In insert(). An exception of type {0} occurred."
                message = template.format(str(e))
                logging.debug(message)
                
def collect(auth, tweet_ids, out_filename):
    api_auth = tweepy.OAuthHandler(auth['consumer_key'], auth['consumer_secret'])
    api_auth.set_access_token(auth['access_token'], auth['access_token_secret'])
    api = tweepy.API(api_auth)
    
    if api.verify_credentials:
        print('Successfully authenticated with Twitter.')
    else:
        print('Failed to authenticate with Twitter. Please try again.')
        sys.exit(1)
    
    outfile = open(out_filename, 'w')
    
    for tweet_id in tweet_ids:
        print('Searching for', tweet_id)
        tweet = api.get_status(tweet_id)
        
        if tweet:
            try:
                status = tweet._json
                status['display_text_range'] = len(status['text'])
                status['full_text'] = status['text']
                outfile.write(json.dumps(status).encode('utf-8').decode('utf-8'))
                outfile.write('\n')
            except TweepError as e:
                err_code = e.api_code
                if 500 <= err_code <= 510:
                    print("Error {} occurred. Waiting for 5 minutes.")
                    logging.debug("Error {} occurred. Waiting for 5 minutes.")
                    time.sleep(60 * 5)
                else:
                    return [eval(e.reason)[0]['message'], ' ', ' ']

            except StopIteration as e:
                collecting = False
                template = "In collect(). An exception of type {0} occurred."
                message = template.format(str(e))
                logging.debug(message)

def run_status(): 
    all_ids = read_input(cfg.INPUT_FILENAME)
    print("Found total of {} IDs.".format(len(all_ids)))
    
    print('Now Collecting...')
    collect(cfg.AUTH, all_ids, cfg.OUTPUT_FILENAME)
    
    print('Now inserting...')
    run_insert(cfg.OUTPUT_FILENAME)
    print('Insertion completed')

