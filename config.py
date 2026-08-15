import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load variables from the .env file
load_dotenv()

APP_TITLE = "ResearchX"
APP_SUBTITLE = "AI Research & Paper Intelligence Assistant"

# Check that the Groq API key exists
if not os.getenv("GROQ_API_KEY"):
    raise RuntimeError(
        "GROQ_API_KEY is missing. Add it to your .env file."
    )

# Initialize the Groq model directly
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)