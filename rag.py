from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.readers.file import XMLReader

data_path = "/mnt/rds/redhen/gallina/projects/ChattyAI/FramesConstructions/fndata-1.7/frame"

parser = XMLReader()
file_extractor = {".xml": parser}
documents = SimpleDirectoryReader(
    data_path, file_extractor=file_extractor
).load_data()

index = VectorStoreIndex.from_documents(documents)

query_engine = index.as_query_engine()
response = query_engine.query("In the FrameNet dataset, what are the FEs for the frame Execute_plan?")
print(response)