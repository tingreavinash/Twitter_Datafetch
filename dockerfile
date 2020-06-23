FROM python:3
ADD config.json DownloadNLTKPackages.py TweetFetch.py /Avinash/
RUN pip install tweepy
RUN pip install nltk
RUN python -m nltk.downloader vader_lexicon
RUN python -m nltk.downloader punkt
WORKDIR /Avinash