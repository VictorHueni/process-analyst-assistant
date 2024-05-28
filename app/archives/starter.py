import os.path
from pprint import pprint

from dotenv import load_dotenv
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)
from llama_index.llms.openai import OpenAI
from llama_index.core.chat_engine import SimpleChatEngine
from llama_index.core.memory import ChatMemoryBuffer

persist_dir = app.config['PERSIST_DIR']


#LLM model defined:
llm = OpenAI(model="gpt-3.5-turbo-0613")

if not os.path.exists(PERSIST_DIR):
    # load the documents and create the index
    documents = SimpleDirectoryReader('./data').load_data()
    index = VectorStoreIndex.from_documents(documents, show_progress=True)
    # store it for later
    index.storage_context.persist(persist_dir=PERSIST_DIR)
else:
    # load the existing index
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)



#Chat engine in a context mode:
memory = ChatMemoryBuffer.from_defaults(token_limit=1500)
chat_engine = index.as_chat_engine(
    chat_mode="context",
    memory=memory,
    system_prompt=(
        "You are a chatbot, able to have normal interactions, as well as read, understand"
        " and analyze restaurant business process called 'PRÉPARER DES PLATS'."
        " You are also well versed in BPMNN Notation and you're able to generate BPMN XML code according to the specification."
    ),
)

# Interactive loop to handle user questions
while True:
    user_question = input("Enter your question (type 'exit' to quit): ")
    if user_question.lower() == 'exit':
        print("It was nice talking to you.")
        break
    response_chat = chat_engine.chat(user_question)
    print("Response:", response_chat)

# Either way we can now query the index
'''
query_engine = index.as_query_engine()
response = query_engine.query("Generate a BPMN XML code detailing the sequence of operations for"
                              " a restaurant kitchen process named 'PRÉPARER DES PLATS'."
                              " The process should start with taking orders, followed by food preparation"
                              " by different kitchen brigades, and end with serving the dishes."
                              " Include tasks, start events, end events, and gateways for decision points.")

pprint(response)


# Creating and writing to a file:
response_data = str(response)
filename = "response.xml"
file_path = os.path.join(OUTPUT_DIR, filename)

with open(file_path, 'w', encoding='utf-8') as file:
    file.write(response_data)

print(f"Response saved to {file_path}")
'''


