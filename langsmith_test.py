import os
from dotenv import load_dotenv, find_dotenv
from langchain.chat_models import ChatOpenAI

load_dotenv(find_dotenv(".langsmith_env"))
load_dotenv(find_dotenv())

vars = ["LANGCHAIN_TRACING_V2",
        "LANGCHAIN_ENDPOINT",
        "LANGCHAIN_API_KEY",
        "LANGCHAIN_PROJECT"]

for var in vars:
    print(f"({var}: {os.getenv(var)}")
