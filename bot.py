#!/usr/bin/env python3
"""Real-time X bot posting Bitcoin mining news."""

import os
import time
import argparse
from typing import List, Set

import requests
from requests_oauthlib import OAuth1
from eventregistry import EventRegistry, QueryArticlesIter, QueryItems


def fetch_news(client: EventRegistry) -> List[dict]:
    """Fetch latest Bitcoin mining articles."""
    query = QueryArticlesIter(
        keywords=QueryItems.AND(["Bitcoin mining"]),
        lang="eng",
    )
    return list(query.execQuery(client, sortBy="date", maxItems=50))


def tweet_articles(
    session: requests.Session,
    articles: List[dict],
    posted: Set[str],
    dry_run: bool,
    posted_file: str,
) -> None:
    """Post new articles to X and record URLs."""
    api_url = "https://api.twitter.com/2/tweets"
    for article in articles:
        url = article.get("url")
        if not url or url in posted:
            continue
        text = f"{article.get('title', '')} {url}"
        if dry_run or session is None:
            print(f"Would tweet: {text}")
        else:
            response = session.post(api_url, json={"text": text})
            response.raise_for_status()
        posted.add(url)
        if posted_file:
            with open(posted_file, "a") as fh:
                fh.write(url + "\n")


def main():
    parser = argparse.ArgumentParser(description="Post Bitcoin mining news to X.")
    parser.add_argument('--interval', type=int, default=900, help='Seconds between fetches.')
    parser.add_argument('--once', action='store_true', help='Fetch and post once then exit.')
    parser.add_argument('--dry-run', action='store_true', help='Print tweets instead of posting.')
    parser.add_argument('--posted-file', default='posted_urls.txt', help='File tracking tweeted article URLs.')
    args = parser.parse_args()

    newsapi_key = os.environ.get("NEWSAPI_KEY")
    news_client = EventRegistry(apiKey=newsapi_key)

    session = None
    if not args.dry_run:
        api_key = os.environ["X_API_KEY"]
        api_secret = os.environ["X_API_SECRET"]
        access_token = os.environ["X_ACCESS_TOKEN"]
        access_secret = os.environ["X_ACCESS_SECRET"]
        session = requests.Session()
        session.auth = OAuth1(api_key, api_secret, access_token, access_secret)

    posted: Set[str] = set()
    if args.posted_file and os.path.exists(args.posted_file):
        with open(args.posted_file) as fh:
            posted = {line.strip() for line in fh if line.strip()}

    while True:
        try:
            articles = fetch_news(news_client)
        except Exception as exc:
            print(f"Error fetching news: {exc}")
            articles = []
        tweet_articles(session, articles, posted, args.dry_run, args.posted_file)
        if args.once:
            break
        time.sleep(args.interval)


if __name__ == '__main__':
    main()
