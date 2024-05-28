import os
from app import app
import logging


from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    StorageContext,
    load_index_from_storage,
    Settings,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_settings():
    model_provider = app.config["MODEL_PROVIDER"]
    if model_provider == "openai":
        init_openai()
    else:
        raise ValueError(f"Invalid model provider: {model_provider}")
    Settings.chunk_size = int(os.getenv("CHUNK_SIZE", "1024"))
    Settings.chunk_overlap = int(os.getenv("CHUNK_OVERLAP", "20"))

def init_openai():
    from llama_index.llms.openai import OpenAI
    from llama_index.embeddings.openai import OpenAIEmbedding
    from llama_index.core.constants import DEFAULT_TEMPERATURE

    try:
        max_tokens = os.getenv("LLM_MAX_TOKENS")
        config = {
            "model": os.getenv("MODEL"),
            "temperature": float(os.getenv("LLM_TEMPERATURE", DEFAULT_TEMPERATURE)),
            "max_tokens": int(max_tokens) if max_tokens is not None else None,
        }
        Settings.llm = OpenAI(**config)

        dimensions = os.getenv("EMBEDDING_DIM")
        config = {
            "model": os.getenv("EMBEDDING_MODEL"),
            "dimensions": int(dimensions) if dimensions is not None else None,
        }
        Settings.embed_model = OpenAIEmbedding(**config)
    except Exception as e:
        logger.error(f"Error initializing OpenAI settings: {e}")
        raise

def get_index():
    index_dir = app.config["PERSIST_DIR"]
    data_dir = app.config["DATA_DIR"]

    try:
        if os.path.exists(index_dir):
            logger.info('Index exists')
            storage_context = StorageContext.from_defaults(persist_dir=index_dir)
            index = load_index_from_storage(storage_context)
        else:
            logger.info("Index doesn't exist, creating index ...")
            storage_context = StorageContext.from_defaults()
            documents = SimpleDirectoryReader(data_dir).load_data()
            index = VectorStoreIndex.from_documents(
                documents, storage_context=storage_context, show_progress=True
            )
            storage_context.persist(persist_dir=index_dir)
    except Exception as e:
        logger.error(f"Error getting or creating index: {e}")
        raise

    return index
