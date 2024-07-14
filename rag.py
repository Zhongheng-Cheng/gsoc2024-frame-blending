import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

import os.path

from dotenv import load_dotenv
load_dotenv()
from os import getenv
from huggingface_hub import login 
login(token=getenv("HUGGINGFACE_API_KEY"))

from models import llama2_llamaindex, embed_model
from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex, StorageContext, load_index_from_storage
from llama_index.readers.json import JSONReader

def get_query_engine(save_index=True):
    Settings.llm = llama2_llamaindex()
    Settings.embed_model = embed_model()
    PERSIST_DIR = "./query_engine.index"
    if os.path.exists(PERSIST_DIR):
        storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
        index = load_index_from_storage(storage_context)
        print(f"Loaded model from {PERSIST_DIR}")
    else:
        parser = JSONReader()
        file_extractor = {".json": parser}
        documents = SimpleDirectoryReader("frame_json/", file_extractor=file_extractor).load_data()
        print("Finished loading data")

        index = VectorStoreIndex.from_documents(documents)
        print("Finished creating index")
        if save_index:
            index.storage_context.persist(persist_dir=PERSIST_DIR)
            print(f"Finished saving index to {PERSIST_DIR}")

    query_engine = index.as_query_engine()
    print("Finished creating query engine")
    return query_engine


def generate_response(query_engine, prompt):
    response = query_engine.query(prompt)
    print(">>> prompt")
    print(prompt)
    print(">>> response")
    print(response)
    return


def multi_conversation(query_engine):
    previous_conversations = []
    while True:
        prompt = input(">>> Prompt: ")
        previous_conversations.append({
            "role": "user",
            "content": prompt
        })
        formatted_conversations = "\n".join(
            [f"User: {conv['content']}" if conv['role'] == "user" else f"Assistant: {conv['content']}" for conv in previous_conversations]
        )
        full_prompt = f"{formatted_conversations}\nUser: {prompt}\nAssistant:"
        response = query_engine.query(full_prompt)
        previous_conversations.append({
            "role": "assistant",
            "content": response
        })
        print(full_prompt)
        print(response)
    return 

