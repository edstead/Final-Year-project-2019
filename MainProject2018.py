import sys,tweepy,csv,re
from textblob import TextBlob
import matplotlib.pyplot as plt
import mysql.connector
from flask import Flask, render_template, request, url_for, redirect


conn = mydb = mysql.connector.connect(host="edstead.mysql.pythonanywhere-services.com", port=3306, user="edstead", passwd="Eddyiscool123", database="edstead$project", use_unicode=True, charset='utf8mb4')


pos = 0
neg = 0
neut = 0


def neutral1(tweet, q):
    conn = mysql.connector.connect(host="edstead.mysql.pythonanywhere-services.com", port=3306, user="edstead", passwd="Eddyiscool123", database="edstead$project", use_unicode=True, charset='utf8mb4')
    Sentiment = "Neutral"
    mycursor = conn.cursor()
    sql = """INSERT INTO project (Keyword, Sentiment,Tweet) VALUES(%s,%s,%s)"""
    val = (q, Sentiment, tweet)

    mycursor.execute(sql, val)
    conn.commit()


def positive1(tweet, q):
    conn = mysql.connector.connect(host="edstead.mysql.pythonanywhere-services.com", port=3306, user="edstead", passwd="Eddyiscool123", database="edstead$project", use_unicode=True, charset='utf8mb4')
    Sentiment = "Positive"
    mycursor = conn.cursor()

    sql = """INSERT INTO project (Keyword, Sentiment,Tweet) VALUES(%s,%s,%s)"""
    val = (q, Sentiment, tweet)

    mycursor.execute(sql, val)
    conn.commit()


def negative1(tweet, q):
    conn = mysql.connector.connect(host="edstead.mysql.pythonanywhere-services.com", port=3306, user="edstead", passwd="Eddyiscool123", database="edstead$project", use_unicode=True, charset='utf8mb4')
    Sentiment = "Negative"
    mycursor = conn.cursor()

    sql = """INSERT INTO project (Keyword, Sentiment,Tweet) VALUES(%s,%s,%s)"""
    val = (q, Sentiment, tweet)

    mycursor.execute(sql, val)
    conn.commit()



class SentimentAnalysis():

    def __init__(self):
        self.tweets = []
        self.tweetText = []

    def DownloadData(self, a, b,):
        # authenticating
        consumerKey = 'fP20pja8Co8xYIdTmcexyU579'
        consumerSecret = '5wFv34bF1Jc6n7oVRkBRsOgB9D6mtYME1YyE40kZf7MmvVmjHK'
        accessToken = '606708487-NystO5Lt08aQYbGYgSb22SMOL1A77QOx3VLgfFlp'
        accessTokenSecret = '1dZfIxdbYP6LEWPTcxHNyYcghXyisTOycWMNcCB2RyoSR'
        auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
        auth.set_access_token(accessToken, accessTokenSecret)
        api = tweepy.API(auth)

        # input for term to be searched and how many tweets to search
        #searchTerm = input("Enter Keyword/Tag to search about: ")
        #NoOfTerms = int(input("Enter how many tweets to search: "))

        searchTerm = a
        NoOfTerms = b
        print(searchTerm)
        print(NoOfTerms)
        NoOfTerms=int(NoOfTerms)

        # searching for tweets
        self.tweets = tweepy.Cursor(api.search, q=searchTerm, lang = "en").items(NoOfTerms)



        # Open/create a file to append data to
        csvFile = open('results.csv', 'a')

        # Use csv writer
        csvWriter = csv.writer(csvFile)


        # creating some variables to store info
        polarity = 0
        positive = 0
        negative = 0
        neutral = 0


        # iterating through tweets fetched
        for tweet in self.tweets:
            finished=0
            #Append to temp so that we can store in csv later. I use encode UTF-8
            self.tweetText.append(self.cleanTweet(tweet.text).encode('utf-8'))
            print(tweet)    #print tweet's text
            analysis = TextBlob(tweet.text)
            print(analysis.sentiment)  # print tweet's polarity
            polarity += analysis.sentiment.polarity  # adding up polarities to find the average later




            if (analysis.sentiment.polarity == 0):  # adding reaction of how people are reacting to find average later
                neutral1(tweet.text, searchTerm)    #function call for saving to database
                neutral += 1
            elif (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 1):
                positive1(tweet.text, searchTerm)   #function call for saving to database
                positive += 1
            elif (analysis.sentiment.polarity > -1 and analysis.sentiment.polarity <= 0):
                negative1(tweet.text, searchTerm)   #function call for saving to database
                negative += 1

        conn.close()





        # Write to csv and close csv file
        csvWriter.writerow(self.tweetText)
        csvFile.close()

        # finding average of how people are reacting
        positive = self.percentage(positive, NoOfTerms)
        negative = self.percentage(negative, NoOfTerms)
        neutral = self.percentage(neutral, NoOfTerms)


        # finding average reaction
        polarity = polarity / NoOfTerms

        # printing out data
        print("How people are reacting on " + searchTerm + " by analyzing " + str(NoOfTerms) + " tweets.")
        print()
        print("General Report: ")

        if (polarity == 0):
            print("Neutral")
        elif (polarity > 0 and polarity <= 1):
            print("Positive")
        elif (polarity > -1 and polarity <= 0):
            print("Negative")

        print()
        print("Report: ")
        print(str(positive) + "% people thought it was positive")
        print(str(negative) + "% people thought it was negative")
        print(str(neutral) + "% people thought it was neutral")

        global pos
        pos = positive
        global neg
        neg = negative

        global neut
        neut = neutral


        self.plotPieChart(positive,  negative, neutral, searchTerm, NoOfTerms)

        finished = 1
        return finished

    def cleanTweet(self, tweet):
        # Remove Links, Special Characters etc from tweet
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

    # function to calculate percentage
    def percentage(self, part, whole):
        temp = 100 * float(part) / float(whole)
        return format(temp, '.2f')

    def plotPieChart(self, positive, negative, neutral, searchTerm, noOfSearchTerms):
        labels = ['Positive [' + str(positive) + '%]', 'Neutral [' + str(neutral) + '%]',
                  'Negative [' + str(negative) + '%]']
        sizes = [positive, neutral, negative, ]
        colors = ['green', 'gold', 'red']
        patches, texts = plt.pie(sizes, colors=colors, startangle=90)
        plt.legend(patches, labels, loc="best")
        plt.title('How people are reacting on ' + searchTerm + ' by analyzing ' + str(noOfSearchTerms) + ' Tweets.')
        plt.axis('equal')
        plt.tight_layout()
        plt.show()





# def runfunc(a, b):
#     searchTerm = a
#     NoOfTerms = b
#     print(searchTerm)
#     print(NoOfTerms)
#     sa = SentimentAnalysis()
#     sa.DownloadData()

def runfunc(a, b):
    searchTerm = a
    NoOfTerms = b
    print(searchTerm)
    print(NoOfTerms)
    sa = SentimentAnalysis()
    sa.DownloadData(searchTerm, NoOfTerms)



# if __name__== "__main__":
#     run_func()
#
#     #app.run()
#     sa = SentimentAnalysis()
#     sa.DownloadData()