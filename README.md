# SHA256NewsBot

A real-time X bot that shares news about Bitcoin mining.

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Set the following environment variables with your credentials:

- `NEWSAPI_KEY` – API key from [NewsAPI.ai](https://newsapi.ai/intro-python)
- `X_API_KEY`
- `X_API_SECRET`
- `X_ACCESS_TOKEN`
- `X_ACCESS_SECRET`

## Usage

Run the bot continuously:

```bash
python bot.py
```

To test without posting tweets and exit after one fetch:

```bash
python bot.py --once --dry-run
```
