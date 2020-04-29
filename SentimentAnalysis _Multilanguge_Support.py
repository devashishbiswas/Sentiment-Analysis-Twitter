import sys,tweepy,csv,re
from textblob import TextBlob
import matplotlib.pyplot as plt
from googletrans import Translator
import emoji

class SentimentAnalysis:

    def __init__(self):
        self.tweets = []
        self.tweetText = []
        self.tweetsInEnglish = []
        #self.translator = Translator()
        self.allTweetsInEnglish = []

    def downloadAndProcessData(self):        

        # Get authentication of your twitter application
        twitterAPI = self.twitterApplicationAuthentication()
        
        # input for term to be searched and how many tweets to search
        searchTerm = input("Enter Keyword/Tag to search about: ")
        noOfTweetsToProcess = int(input("Enter how many tweets to process: "))

        # searching for tweets
        self.tweets = tweepy.Cursor(twitterAPI.search, q=searchTerm, lang = "de").items(noOfTweetsToProcess)
        
        # Translate Non english tweets in English for sentiment Analysis
        self.tweetsInEnglish = self.translateNonEnglishTweetsToEnglish(self.tweets)
        

        # Open/create a file to append data to
        csvFile = open('twitterData.csv', 'a')

        # Use csv writer
        csvWriter = csv.writer(csvFile)


        # creating some variables to store info
        polarity = 0
        positive = 0
        wpositive = 0
        spositive = 0
        negative = 0
        wnegative = 0
        snegative = 0
        neutral = 0


        print(self.tweetsInEnglish)
        # iterating through the translated tweets 
        for tweet in self.tweetsInEnglish:
            print(tweet)
            #Append to temp so that we can store in csv later. I use encode UTF-8
            self.tweetText.append(self.cleanTweet(tweet).encode('utf-8'))
            #print (tweet.text.translate(non_bmp_map))  
            
            analysis = TextBlob(tweet)
            # print(analysis.sentiment)  # print tweet's polarity
            polarity += analysis.sentiment.polarity  # adding up polarities to find the average later

            if (analysis.sentiment.polarity == 0):  # adding reaction of how people are reacting to find average later
                neutral += 1
            elif (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 0.3):
                wpositive += 1
            elif (analysis.sentiment.polarity > 0.3 and analysis.sentiment.polarity <= 0.6):
                positive += 1
            elif (analysis.sentiment.polarity > 0.6 and analysis.sentiment.polarity <= 1):
                spositive += 1
            elif (analysis.sentiment.polarity > -0.3 and analysis.sentiment.polarity <= 0):
                wnegative += 1
            elif (analysis.sentiment.polarity > -0.6 and analysis.sentiment.polarity <= -0.3):
                negative += 1
            elif (analysis.sentiment.polarity > -1 and analysis.sentiment.polarity <= -0.6):
                snegative += 1


        # Write to csv and close csv file
        csvWriter.writerow(self.tweetText)
        csvFile.close()

        # finding average of how people are reacting
        positive = self.percentage(positive, noOfTweetsToProcess)
        wpositive = self.percentage(wpositive, noOfTweetsToProcess)
        spositive = self.percentage(spositive, noOfTweetsToProcess)
        negative = self.percentage(negative, noOfTweetsToProcess)
        wnegative = self.percentage(wnegative, noOfTweetsToProcess)
        snegative = self.percentage(snegative, noOfTweetsToProcess)
        neutral = self.percentage(neutral, noOfTweetsToProcess)

        # finding average reaction
        polarity = polarity / noOfTweetsToProcess
        
        print ("Polarity of report : " +str(polarity))

        # printing out data
        print("How people are reacting on " + searchTerm + " by analyzing " + str(noOfTweetsToProcess) + " tweets.")
        print()
        print("General Report: ")

        if (polarity == 0):
            print("Neutral")
        elif (polarity > 0 and polarity <= 0.3):
            print("Weakly Positive")
        elif (polarity > 0.3 and polarity <= 0.6):
            print("Positive")
        elif (polarity > 0.6 and polarity <= 1):
            print("Strongly Positive")
        elif (polarity > -0.3 and polarity <= 0):
            print("Weakly Negative")
        elif (polarity > -0.6 and polarity <= -0.3):
            print("Negative")
        elif (polarity > -1 and polarity <= -0.6):
            print("Strongly Negative")

        print()
        print("Detailed Report: ")
        print(str(positive) + "% people thought it was positive")
        print(str(wpositive) + "% people thought it was weakly positive")
        print(str(spositive) + "% people thought it was strongly positive")
        print(str(negative) + "% people thought it was negative")
        print(str(wnegative) + "% people thought it was weakly negative")
        print(str(snegative) + "% people thought it was strongly negative")
        print(str(neutral) + "% people thought it was neutral")

        self.plotPieChart(positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm, noOfTweetsToProcess)


    def cleanTweet(self, tweet):
        # Remove Links, Special Characters etc from tweet
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())
    
    def translateNonEnglishTweetsToEnglish(self, tweets):        
        for status in tweets:
            status=status._json
            if self.checkTweetLanguage(status):
                #print(status['text'])
                translator = Translator()
                
                # Handling emojis in tweet before translating using googletrans library
                str_demoji = emoji.demojize(status['text'])
                
                #translating non english tweets to english
                tran=translator.translate(str_demoji,dest='en').text
                
                str_emoji = emoji.emojize(tran.replace(': ',':').capitalize())
                print(str_emoji)
                self.allTweetsInEnglish.append(str_emoji)
                #self.allTweetsInEnglish.append(self.translator.translate(status['text']).text)

            else:
                self.allTweetsInEnglish.append(status['text'])
        return self.allTweetsInEnglish
            
    
    # function to check the tweet language
    def checkTweetLanguage(self , status):
        return status['lang'] != 'en'
            
    # function to Authenticate Twitter Application
    def twitterApplicationAuthentication(self):
        # Twitter Authentication for application
        consumerKey = 'Your Key Here'
        consumerSecret = 'Your Key Here'
        accessToken = 'Your Key Here'
        accessTokenSecret = 'Your Key Here'
        auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
        auth.set_access_token(accessToken, accessTokenSecret)
        return tweepy.API(auth)       

    # function to calculate percentage
    def percentage(self, part, whole):
        temp = 100 * float(part) / float(whole)
        return format(temp, '.2f')

    # function to plot pie chart
    def plotPieChart(self, positive, wpositive, spositive, negative, wnegative, snegative, neutral, searchTerm, noOfTweetsToProcess):
        labels = ['Positive [' + str(positive) + '%]', 'Weakly Positive [' + str(wpositive) + '%]','Strongly Positive [' + str(spositive) + '%]', 'Neutral [' + str(neutral) + '%]',
                  'Negative [' + str(negative) + '%]', 'Weakly Negative [' + str(wnegative) + '%]', 'Strongly Negative [' + str(snegative) + '%]']
        sizes = [positive, wpositive, spositive, neutral, negative, wnegative, snegative]
        colors = ['yellowgreen','lightgreen','darkgreen', 'gold', 'red','lightsalmon','darkred']
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.title('How people are reacting on ' + searchTerm + ' by analyzing ' + str(noOfTweetsToProcess) + ' Tweets.')
        plt.axis('equal')
        plt.tight_layout()
        plt.show()



if __name__== "__main__":
    sa = SentimentAnalysis()
    sa.downloadAndProcessData()