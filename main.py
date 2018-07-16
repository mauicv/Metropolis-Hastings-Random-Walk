'''
Created on 13 Feb 2017

@author: mauicv
'''
import tweepy 
from tweepy import OAuthHandler
from MHRW_Algo.Collection import Collection
from MHRW_Algo.MH_random_walk import MHRW

import time

consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)
                   
if __name__ == '__main__':
    
    #seedUser=api.get_user(screen_name="ManancialBiblic")
    #randomWalk=MHRW(api=api,seed=seedUser,data_file='data')
    randomWalk=MHRW(api=api,data_file='data')
    #user=randomWalk.collection.getLast()
    then = time.time() #Time before the operations start
    randomWalk.run(500)
    now = time.time() #Time after it finished
    print("It took: ", now-then, " seconds")
    
    #randomWalk=MHRW(api=api,data_file='data')
    randomWalk.printAllProg()
        
        
    