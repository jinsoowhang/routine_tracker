# openai_helper.py
from openai import OpenAI
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

def dataframe_to_text_summary(df: pd.DataFrame, max_rows=30) -> str:
    """
    Convert a DataFrame to a readable string summary.
    Limits to max_rows for brevity.
    """
    if df.empty:
        return "No data available."
    
    # Take the first max_rows rows and convert to markdown-like table
    limited_df = df.head(max_rows)
    return limited_df.to_string(index=False)

def ask_openai_chat(prompt: str, context_df: pd.DataFrame = None, model="gpt-4o-mini") -> str:
    """
    Send a prompt to OpenAI chat completions with optional DataFrame context.
    Returns the response text.
    """
    context_text = ""
    if context_df is not None:
        context_text = dataframe_to_text_summary(context_df)
    
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant who answers questions based on the provided data. "
                "Here is the data context:\n" + context_text
            ),
        },
        {"role": "user", "content": prompt},
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    return response.choices[0].message.content