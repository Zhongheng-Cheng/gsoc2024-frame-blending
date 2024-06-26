import logging
import sys
from os import getenv

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


from huggingface_hub import login 
login(token=getenv("HUGGINGFACE_API_KEY"))

import torch
from llama_index.llms.huggingface import HuggingFaceLLM
from llama_index.core import PromptTemplate

# Model names (make sure you have access on HF)
LLAMA2_7B = "meta-llama/Llama-2-7b-hf"
LLAMA2_7B_CHAT = "meta-llama/Llama-2-7b-chat-hf"
LLAMA2_13B = "meta-llama/Llama-2-13b-hf"
LLAMA2_13B_CHAT = "meta-llama/Llama-2-13b-chat-hf"
LLAMA2_70B = "meta-llama/Llama-2-70b-hf"
LLAMA2_70B_CHAT = "meta-llama/Llama-2-70b-chat-hf"

selected_model = LLAMA2_7B_CHAT

SYSTEM_PROMPT = """You are an AI assistant in linguistics that answers questions about frame blending. Here are some rules you always follow:
- Generate human readable output, avoid creating output with gibberish text.
- Generate only the requested output, don't include any other language before or after the requested output.
- Never say thank you, that you are happy to help, that you are an AI agent, etc. Just answer directly.
- Generate professional language typically used in business documents in North America.
- Never generate offensive or foul language.
- Use terminology that aligns with given source documents which are all the frame dataset of FrameNet.
"""

query_wrapper_prompt = PromptTemplate(
    "[INST]<<SYS>>\n" + SYSTEM_PROMPT + "<</SYS>>\n\n{query_str}[/INST] "
)

llm = HuggingFaceLLM(
    context_window=4096,
    max_new_tokens=2048,
    generate_kwargs={"temperature": 0.9, "do_sample": True},
    query_wrapper_prompt=query_wrapper_prompt,
    tokenizer_name=selected_model,
    model_name=selected_model,
    device_map="auto",
    # change these settings below depending on your GPU
    model_kwargs={"torch_dtype": torch.float16, "load_in_8bit": True},
)

from llama_index.embeddings.huggingface import HuggingFaceEmbedding

embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

from llama_index.core import Settings

Settings.llm = llm
Settings.embed_model = embed_model


from llama_index.core import SimpleDirectoryReader
from llama_index.readers.file import XMLReader

parser = XMLReader()
file_extractor = {".xml": parser}

# load documents
documents = SimpleDirectoryReader("../../frame/", file_extractor=file_extractor).load_data()

print("Finished loading data")

from llama_index.core import VectorStoreIndex

index = VectorStoreIndex.from_documents(documents)

# set Logging to DEBUG for more detailed outputs
query_engine = index.as_query_engine()

# prompt = '''Please randomly pick two frames from the FrameNet dataset, and tell me what you have picked. Then, generate an example of frame blending with the two frames that you picked, along with the analysis process similar to the example I provide you. Here is an example of frame blending: 
# # Expression
# "Time is money."
# # Frames Involved:
# ## Time Frame
# This involves concepts related to the passage of time, such as hours, minutes, schedules, deadlines, etc.
# ## Money Frame
# This involves concepts related to financial transactions, value, budgeting, saving, spending, etc.
# # Analysis of the Frame Blending
# ## Input Spaces
# Time: The source frame includes elements like seconds, hours, schedules, deadlines, etc.
# Money: The target frame includes elements like currency, investment, expenses, profit, loss, etc.
# ## Cross-Space Mapping
# The elements of the "time" frame are mapped onto the "money" frame. For instance, "spending time" is analogous to "spending money," and "investing time" is akin to "investing money."
# ## Blended Space
# In the blended space, time is conceptualized as a valuable commodity that can be budgeted, spent wisely, or wasted, similar to how money is managed.
# # Emergent Structure
# This blend creates a new understanding where activities are seen through the lens of financial transactions. For example, "wasting time" implies a loss similar to wasting money, highlighting the value and scarcity of time.'''

# prompt = '''Please read the provided FrameNet data, then answer this question: what is the definition of the frame 'Execute_plan'?'''

# prompt = '''Please read the frame 'Execute_plan' in the provided FrameNet data, then describe the frame in terms of its definition, frame elements and other frame relations with it.'''

# prompt = '''Please read the frame 'Execute_plan', then generate a sentence based on the frame. Relate all the sentence parts with the frame elements.'''

# prompt = '''Please read the frame 'physics' and 'family', then generate a frame blending sentence based on two frames. Provide an analysis according to the sentence that you generated.'''

prompt = '''Please read the frame 'beauty', 'death' and 'kinship', then generate a frame blending sentence based on two frames. Provide an analysis according to the sentence that you generated.
Here is an example of frame blending, you should follow this process while generating, but not use this example:
# Expression
"Time is money."
# Frames Involved:
## Time Frame
This involves concepts related to the passage of time, such as hours, minutes, schedules, deadlines, etc.
## Money Frame
This involves concepts related to financial transactions, value, budgeting, saving, spending, etc.
# Analysis of the Frame Blending
## Input Spaces
Time: The source frame includes elements like seconds, hours, schedules, deadlines, etc.
Money: The target frame includes elements like currency, investment, expenses, profit, loss, etc.
## Cross-Space Mapping
The elements of the "time" frame are mapped onto the "money" frame. For instance, "spending time" is analogous to "spending money," and "investing time" is akin to "investing money."
## Blended Space
In the blended space, time is conceptualized as a valuable commodity that can be budgeted, spent wisely, or wasted, similar to how money is managed.
# Emergent Structure
This blend creates a new understanding where activities are seen through the lens of financial transactions. For example, "wasting time" implies a loss similar to wasting money, highlighting the value and scarcity of time.'''

response = query_engine.query(prompt)
print(response)