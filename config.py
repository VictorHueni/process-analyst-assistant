import os
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    # check if storage already exists
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DATA_DIR = os.path.abspath(os.getenv("DATA_DIR"))
    PERSIST_DIR = os.path.abspath(os.getenv("PERSIST_DIR"))
    OUTPUT_DIR = os.path.abspath(os.getenv("OUTPUT_DIR"))
    LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS"))
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_ORG_ID = os.getenv("OPENAI_ORG_ID")
