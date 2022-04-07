# 🤖 Ezil Stats telegram bot

Telegram bot for tracking stats on ezil.me mining pool.

## ⚙ Configuration

In the environment variables, you need to put the bot's API token

`TELEGRAM_API_TOKEN` — API bot token

Usage with Docker is shown below. Fill in the ENV variables in the Dockerfile

```
docker build -t ezil_stats ./

docker run -d --name bot ezil_stats
```

To enter a working container:

```
docker exec -ti bot bash
```