#!/usr/bin/env python3
"""Real-time Twitter bot posting Bitcoin mining news."""

import os
import time
import argparse
from typing import Set

from newsapi import NewsApiClient
import tweepy


def fetch_news(client: NewsApiClient):
    """Fetch latest Bitcoin mining articles."""
    articles = client.get_everything(q='"Bitcoin mining"', language='en', sort_by='publishedAt')
    return articles.get('articles', [])


def tweet_articles(client: tweepy.Client, articles, posted: Set[str], dry_run: bool):
    """Post new articles to Twitter."""
    for article in articles:
        url = article.get('url')
        if not url or url in posted:
            continue
        status = f"{article.get('title', '')} {url}"
        if dry_run:
            print(f"Would tweet: {status}")
        else:
            client.create_tweet(text=status)
        posted.add(url)


def main():
    parser = argparse.ArgumentParser(description='Post Bitcoin mining news to Twitter.')
    parser.add_argument('--interval', type=int, default=900, help='Seconds between fetches.')
    parser.add_argument('--once', action='store_true', help='Fetch and post once then exit.')
    parser.add_argument('--dry-run', action='store_true', help='Print tweets instead of posting.')
    args = parser.parse_args()

    newsapi_key = os.environ['NEWSAPI_KEY']
    twitter_api_key = os.environ['TWITTER_API_KEY']
    twitter_api_secret = os.environ['TWITTER_API_SECRET']
    twitter_access_token = os.environ['TWITTER_ACCESS_TOKEN']
    twitter_access_secret = os.environ['TWITTER_ACCESS_SECRET']

    news_client = NewsApiClient(api_key=newsapi_key)
    twitter_client = tweepy.Client(
        consumer_key=twitter_api_key,
        consumer_secret=twitter_api_secret,
        access_token=twitter_access_token,
        access_token_secret=twitter_access_secret,
    )

    posted: Set[str] = set()

    while True:
        articles = fetch_news(news_client)
        tweet_articles(twitter_client, articles, posted, args.dry_run)
        if args.once:
            break
        time.sleep(args.interval)


if __name__ == '__main__':
    main()
