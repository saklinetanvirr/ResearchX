import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq


load_dotenv()


APP_TITLE = "ResearchX"


GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY"
)


llm = ChatGroq(

    model="openai/gpt-oss-20b",

    temperature=0,

    streaming=True,

    api_key=GROQ_API_KEY,

    timeout=120,

    max_retries=3

)