import tweepy
import urllib3
import csv
import json
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Disabling warning due to SSL
urllib3.disable_warnings()


# Function to decide the sentiment of given text
def sentiment_analyze(text):
    sid = SentimentIntensityAnalyzer()
    scores = sid.polarity_scores(text)
    return scores['compound']


# Function to fetch tweets using given handle
def get_tweets(username, limit, outputfile):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)

    try:
        # Authenticate the API using given keys
        api = tweepy.API(auth)
        tweets = api.user_timeline(screen_name=username, count=limit)
    except Exception as e:
        print(e)
        return ""

    tmp = []
    array_of_tweets = [tweet.text for tweet in tweets]
    with open(outputfile, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["SerialNo", "Tweet", "Type"])
        counter = 0
        for j in array_of_tweets:
            counter = counter + 1
            tmp.append(j)
            score = sentiment_analyze(j)
            if score > 0:
                tweettype = "Positive"
            elif score < 0:
                tweettype = "Negetive"
            else:
                tweettype = "Neutral"
            writer.writerow([counter, j, tweettype])
    return tmp


def read_config():
    config = {};
    try:
        with open('config.json') as f:
            data = json.load(f)
            config["tweet_fetch_limit"] = data["tweet_fetch_limit"]
            config["twitter_handle"] = data["twitter_handle"]
            config["output_file"] = data["output_file"]
            config["consumer_key"] = data["consumer_key"]
            config["consumer_secret"] = data["consumer_secret"]
            config["access_key"] = data["access_key"]
            config["access_secret"] = data["access_secret"]
        config["status"] = "success"
    except Exception as e:
        config["status"] = "failure"
        print(e)
    finally:
        return config


if __name__ == '__main__':

    # Read configuration from JSON file
    result_config = read_config()

    if result_config["status"] == "success":
        tweet_limit = result_config["tweet_fetch_limit"]
        twitter_handle = result_config["twitter_handle"]
        outputFile = result_config["output_file"]
        consumer_key = result_config["consumer_key"]
        consumer_secret = result_config["consumer_secret"]
        access_key = result_config["access_key"]
        access_secret = result_config["access_secret"]

        result = get_tweets(twitter_handle, tweet_limit, outputFile)
        if len(result) > 0:
            print("Total {0} tweets fetched from handle '{1}', Analyzed the sentiment and exported the data to {2}"
                  .format(tweet_limit, twitter_handle, outputFile))
        else:
            print("Caught error which fetching tweets !")
    else:
        print("Error reading config file.")