import os
from app import app
from app.index import get_index
import logging

from llama_index.core.storage.chat_store import SimpleChatStore
from llama_index.core.memory import ChatMemoryBuffer


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



def get_chat_engine():
    chat_store = SimpleChatStore()

    chat_memory = ChatMemoryBuffer.from_defaults(
        token_limit=app.config["LLM_MAX_TOKENS"] if app.config["LLM_MAX_TOKENS"] is not None else None,
        chat_store=chat_store,
        chat_store_key="user1",
    )

    system_prompt = os.getenv("SYSTEM_PROMPT")
    top_k = os.getenv("TOP_K", 3)

    index = get_index()
    if index is None:
        raise ValueError("Index is not initialized")

    return index.as_chat_engine(
        similarity_top_k=int(top_k),
        system_prompt=system_prompt,
        chat_mode="condense_plus_context",
        verbose=True,
        memory=chat_memory,
    )
