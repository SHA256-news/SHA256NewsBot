# SHA256NewsBot

A real-time Twitter bot that shares news about Bitcoin mining.

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Set the following environment variables with your credentials:

- `NEWSAPI_KEY` – API key from [NewsAPI.ai](https://newsapi.ai/intro-python)
- `TWITTER_API_KEY`
- `TWITTER_API_SECRET`
- `TWITTER_ACCESS_TOKEN`
- `TWITTER_ACCESS_SECRET`

## Usage

Run the bot continuously:

```bash
python bot.py
```

To test without posting tweets and exit after one fetch:

```bash
python bot.py --once --dry-run
```
