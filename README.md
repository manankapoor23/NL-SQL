# NL-SQL
Slack bot that lets you query a SQLite database using plain English. You type a question with `/ask-data`, it converts it to SQL using Google Gemini, runs it, and posts the results back in Slack.

## How it works

1. User sends a slash command like `/ask-data total revenue by region last week`
2. LangChain + Gemini turns that into a SQL query against the `sales_daily` table
3. Query runs on a local SQLite database
4. Results come back formatted in Slack

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file:

```
SLACK_BOT_TOKEN=xoxb-...
SLACK_APP_TOKEN=xapp-...
GEMINI_API_KEY=your-key-here
```

Seed the database:

```bash
python seed_db.py
```

Run:

```bash
python app.py
```

## Project structure

- `app.py` — Slack bot entry point, handles the `/ask-data` command
- `nl_to_sql.py` — Converts natural language to SQL using Gemini
- `db.py` — Runs queries against SQLite
- `formatter.py` — Formats query results into Slack blocks
- `seed_db.py` — Creates and populates the sample database

## Database schema

Single table `sales_daily` with columns: `date`, `region`, `category`, `revenue`, `orders`.

## Requirements

- Python 3.10+
- A Slack app with socket mode enabled and the `/ask-data` slash command configured
- Google Gemini API key