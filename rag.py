import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

from os import getenv
from huggingface_hub import login 
login(token=getenv("HUGGINGFACE_API_KEY"))

from models import llama2_ollama, embed_model
from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex
from llama_index.readers.file import XMLReader

# Settings.llm = llama2_ollama()
# Settings.embed_model = embed_model()

parser = XMLReader()
file_extractor = {".xml": parser}
documents = SimpleDirectoryReader("frame_tmp/", file_extractor=file_extractor).load_data()
print("Finished loading data")

index = VectorStoreIndex.from_documents(documents)

# set Logging to DEBUG for more detailed outputs
query_engine = index.as_query_engine()

one_shot_example = '''Here is an example of frame blending, you should follow this process while generating, but not use this example:
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
The elements of the "time" frame are mapped onto the "money" frame. 
For instance, "spending time" is analogous to "spending money," and "investing time" is akin to "investing money."
## Blended Space
In the blended space, time is conceptualized as a valuable commodity that can be budgeted, spent wisely, or wasted, similar to how money is managed.
# Emergent Structure
This blend creates a new understanding where activities are seen through the lens of financial transactions. 
For example, "wasting time" implies a loss similar to wasting money, highlighting the value and scarcity of time.
'''

prompt_random_pick = f'''Please randomly pick two frames from the FrameNet dataset, and tell me what you have picked.
Then, generate an example of frame blending with the two frames that you picked, 
along with the analysis process similar to the example I provide you.
{one_shot_example}
'''

prompt_definition = f'''Please read the provided FrameNet data, 
then answer this question: what is the definition of the frame 'Execute_plan'?
'''

prompt_describe = f'''Please read the frame 'Execute_plan' in the provided FrameNet data,
then describe the frame in terms of its definition, frame elements and other frame relations with it.
'''

prompt_fb_2frames_zeroshot = f'''Please read the frame 'physics' and 'family', 
then generate a frame blending sentence based on two frames. 
Provide an analysis according to the sentence that you generated.
'''

prompt_fb_3frames_oneshot = f'''Please read the frame 'beauty', 'death' and 'kinship', 
then generate a frame blending sentence based on two frames. 
Provide an analysis according to the sentence that you generated.
{one_shot_example}
'''

response = query_engine.query(prompt_fb_3frames_oneshot)
print(response)