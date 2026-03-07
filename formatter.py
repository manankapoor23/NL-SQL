"""
Slack Block Kit formatter.
Turns query results into a clean, readable Slack message.
"""


def format_slack_response(
    question: str,
    sql: str,
    columns: list[str],
    rows: list[list],
    total_count: int,
) -> list[dict]:
    """Build a Slack Block Kit message from query results."""

    if not rows:
        body = "_No rows returned._"
    else:
        header = " | ".join(columns)
        lines = [" | ".join(str(v) for v in row) for row in rows]
        note = (
            f"_Showing {len(rows)} of {total_count} rows_"
            if total_count > len(rows)
            else f"_Showing all {total_count} row(s)_"
        )
        body = f"```{header}\n" + "\n".join(lines) + f"```\n{note}"

    return [
        {"type": "section", "text": {"type": "mrkdwn", "text": f"*🤖 Query Results*\n> {question}"}},
        {"type": "divider"},
        {"type": "section", "text": {"type": "mrkdwn", "text": body}},
        {"type": "divider"},
        {"type": "context", "elements": [{"type": "mrkdwn", "text": f"*SQL:*\n```{sql}```"}]},
    ]