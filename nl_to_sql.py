
import os
import re
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

TABLE_SCHEMA = """
You have access to a single SQLite table:

Table: sales_daily
Columns:
  - date         TEXT          The date of the sales record (format: YYYY-MM-DD)
  - region       TEXT          Sales region (e.g. 'North', 'South', 'East', 'West')
  - category     TEXT          Product category (e.g. 'Electronics', 'Grocery', 'Fashion')
  - revenue      REAL          Total revenue in USD for that day/region/category
  - orders       INTEGER       Number of orders placed
  - created_at   TEXT          Row creation timestamp (rarely needed)

Primary key: (date, region, category)

Sample data:
  date       | region | category    | revenue    | orders
  -----------+--------+-------------+------------+-------
  2025-09-01 | North  | Electronics | 125000.50  | 310
  2025-09-01 | South  | Grocery     |  54000.00  | 820
  2025-09-02 | West   | Fashion     |  45500.00  | 210
"""

SYSTEM_PROMPT = f"""You are a SQL expert. Given a natural language question, generate a single valid SQLite SELECT statement.

{TABLE_SCHEMA}

Rules:
 Output ONLY the raw SQL query — no markdown, no backticks, no explanation.
 Use only the table sales_daily.
 Always use lowercase column names.
 For aggregations, always include a GROUP BY clause.
 Limit results to 50 rows unless the user asks for more.
 Never use INSERT, UPDATE, DELETE, DROP, or any DDL/DML other than SELECT.
"""

HUMAN_TEMPLATE = "Question: {question}"


def generate_sql(question: str) -> str:
    """
    Convert a natural language question to a SQL SELECT statement.

    Args:
        question: The user's natural language question

    Returns:
        A single SQL SELECT statement as a string

    Raises:
        ValueError: If the model returns something that doesn't look like SQL
        Exception: On LLM API errors
    """
    llm = ChatGoogleGenerativeAI(
        model=os.environ.get("GEMINI_MODEL", "gemini-2.0-flash"),
        temperature=0,
        google_api_key=os.environ["GEMINI_API_KEY"],
    )


    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            ("human", HUMAN_TEMPLATE),
        ]
    )

    chain = prompt | llm | StrOutputParser()

    raw_output = chain.invoke({"question": question}).strip()


    sql = _clean_sql(raw_output)


    if not sql.upper().startswith("SELECT"):
        raise ValueError(
            f"Model returned non-SELECT statement. Output: {raw_output[:200]}"
        )

    return sql


def _clean_sql(text: str) -> str:
    """Remove markdown code fences and extra whitespace."""
    # Remove ```sql ... ``` or ``` ... ``` blocks
    text = re.sub(r"```(?:sql)?\s*", "", text)
    text = text.replace("```", "")
    return text.strip()