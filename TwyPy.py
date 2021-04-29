from tweepy import API, Cursor, OAuthHandler, Stream
from tweepy.streaming import StreamListener

import re
import twitter_credentials
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# # # # TWITTER AUTHENTICATOR # # # #
class TwitterAuthenticator():
    
    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitter_credentials.CONSUMER_TOKEN, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_SECRET)
        return auth


# # # # TWITTER CLIENT # # # #
class TwitterClient():
    
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client

    
    def get_user_timeline_tweets(self, num_tweets):
        user_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user, include_rts=False).items(num_tweets):
            user_timeline_tweets.append(tweet.text)
        return user_timeline_tweets
    
    def get_friend_list(self, num_friends):
        friend_list= []
        for friend in Cursor(self.twitter_client.user_friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friends)
        return friend_list
    
    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets

# # # # TWITTER STREAMER # # # #
class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """
    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()

    def stream_tweets(self, fetched_tweets_filename, filter_keyword_list):
        #this handles twitter auth and the connection to the Twitter STreaming API.

        listener = TweetListener(fetched_tweets_filename)
        auth = self.twitter_authenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)

        stream.filter(track=filter_keyword_list)


class TweetListener(StreamListener):
    """
    Listener class that stores tweets in a json file
    """

    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, raw_data):
        try:
            print(raw_data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(raw_data) 
            return True
        except BaseException as e:
            print("Error on TweetListener.on_data: %s" % str(e))
        return True
    
    def on_error(self, status_code):
        if status == 420:
            # Return False on on_data method incase rate limit occurs
            return False
        print(status_code)

    
class TweetAnalyzer():
    """
    Functionality for analyzing and categorizing content from tweets
    """
    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data=[tweet.full_text for tweet in tweets], columns=['Tweets'])

        df['id'] = np.array([tweet.id for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['len'] = np.array([len(tweet.full_text) for tweet in tweets])
        df['place'] = np.array([tweet.created_at for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])
        return df

if __name__ == "__main__":

    twitter_client = TwitterClient("_saintcharles_")
    tweet_analyzer = TweetAnalyzer()
    api = twitter_client.get_twitter_client_api()

    tweets = api.user_timeline(screen_name="_saintcharles_", count=200000, tweet_mode="extended")
    
    #tweets = twitter_client.get_user_timeline_tweets(1000)

    #print(tweets)
    
    df = tweet_analyzer.tweets_to_data_frame(tweets)
    
    print(df)
    
    #### TWEET DATA PLOTTING #####

    # # Get average length over all tweets.
    # print(np.mean(df['len']))

    # # Get num of likes for most liked tweets
    # print(np.max(df['likes']))
    
    # # Get num of retweets for most retweets tweets
    # print(np.max(df['retweets']))

    # # Time Series
    # # time_likes = pd.Series(data=df['likes'].values, index=df['date'])
    # # time_likes.plot(figsize=(16,4), color='b')
    # # plt.show()

    # # Likes V Retweets Time Series
    # time_likes = pd.Series(data=df['likes'].values, index=df['date'])
    # time_likes.plot(figsize=(16,4), label="likes", legend=True)
    
    # time_retweets = pd.Series(data=df['retweets'].values, index=df['date'])
    # time_retweets.plot(figsize=(16,4), label="retweets", legend=True)
    # plt.show()


    # twitter_streamer = TwitterStreamer()
    # twitter_streamer.stream_tweets(fetched_tweets_filename, filter_keyword_list)

    