"""
Slack AI Data Bot - Main Application
Handles /ask-data slash command → NL→SQL via LangChain → Postgres → Slack reply
"""

import os
import logging
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv

from nl_to_sql import generate_sql
from db import execute_query
from formatter import format_slack_response

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = App(token=os.environ["SLACK_BOT_TOKEN"])


@app.command("/ask-data")
def handle_ask_data(ack, respond, command):
    """Handle the /ask-data slash command."""
    # Acknowledge immediately (Slack requires <3s)
    ack()

    question = command.get("text", "").strip()
    user_id = command.get("user_id", "unknown")

    if not question:
        respond(
            text="Please provide a question. Example: `/ask-data show revenue by region for 2025-09-01`"
        )
        return

    logger.info(f"User {user_id} asked: {question}")

    # Step 1: Generate SQL from natural language
    try:
        sql = generate_sql(question)
        logger.info(f"Generated SQL: {sql}")
    except Exception as e:
        logger.error(f"NL→SQL failed: {e}")
        respond(
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"❌ *Failed to generate SQL*\n```{str(e)}```",
                    },
                }
            ]
        )
        return

    # Step 2: Execute SQL against Postgres
    try:
        columns, rows, row_count = execute_query(sql)
        logger.info(f"Query returned {row_count} rows")
    except Exception as e:
        logger.error(f"SQL execution failed: {e}")
        respond(
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"❌ *Query execution failed*\n```{str(e)}```\n\n*Generated SQL:*\n```{sql}```",
                    },
                }
            ]
        )
        return

    # Step 3: Format and send Slack reply
    blocks = format_slack_response(question, sql, columns, rows, row_count)
    respond(blocks=blocks)


if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    logger.info("⚡️ Slack AI Data Bot is running!")
    handler.start()