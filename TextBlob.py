from textblob import TextBlob
import tweepy

Feedback1 ="I am a programmer"
Feedback2 ="The food is not bad"
blob1 = TextBlob(Feedback1)
blob2 = TextBlob(Feedback2)

print(blob1.sentiment)
print(blob2.sentiment)

consumer_key='Add Your Key'
consumer_secret='Add Your Key'
access_token='Add Your Key'
access_token_secret='Add Your Key'
auth=tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)
api=tweepy.API(auth)
public_tweets=api.search('Intelligent Enterprise')
public_tweets
for tweet in public_tweets:
    print(tweet)
    analysis = TextBlob(tweet.text)
    print(analysis.sentiment)