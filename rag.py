import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

from dotenv import load_dotenv
load_dotenv()
from os import getenv
from huggingface_hub import login 
login(token=getenv("HUGGINGFACE_API_KEY"))

from models import llama2_llamaindex, embed_model
from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex
from llama_index.readers.json import JSONReader

Settings.llm = llama2_llamaindex()
Settings.embed_model = embed_model()

parser = JSONReader()
file_extractor = {".json": parser}
documents = SimpleDirectoryReader("frame_json/", file_extractor=file_extractor).load_data()
print("Finished loading data")

index = VectorStoreIndex.from_documents(documents)

# set Logging to DEBUG for more detailed outputs
query_engine = index.as_query_engine()

one_shot_example = '''Here is an example of frame blending analysis, you should follow this analyzing process while generating, but not use this example:
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
then answer this question: what is the definition of the frame 'Abusing'?
'''

prompt_fe = f'''Please read the provided FrameNet data, 
then answer this question: what are the frame elements of the frame 'Abusing'?
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

prompt_type = f'''In the FrameNet dataset, what frames are related to neighborhood?
'''

prompt_cross_mapping = f'''Here is a basic analysis of two frames, please generate a sentence with regard to this blending, and provide the full frame blending analysis.
## Foreign_or_domestic_country Frame
This frame is related to the concept of a country or nation, and its constituent parts, such as population, location, and political status.
## Relation Frame
This involves concepts related to a relation holds between Entity_1 and Entity_2, such as neighborhood, friend, enemy, etc.
# Analysis of the Frame Blending
## Input Spaces
Foreign_or_domestic_country: The source frame includes elements like population, dominition, etc.
Relation: The target frame includes elements like location, positivity, etc.
## Cross-Space Mapping
The elements of the "Foreign_or_domestic_country" frame are mapped onto the "Relation" frame. 
For instance, "relation between two countries" is analogous to "neighborhood between two people", and "attack other countries" is akin to "assult neighbors".
'''

# response = query_engine.query(prompt_cross_mapping)
# print(response)

def multi_conversation():
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

def cot():
    cot_example = f'''
User: Select the relevant FrameNet frames for the following words and generate a frame blending example.
Words: Time, Money

Assistant: Let's think step by step:

Step 1: Think of Frames Involved:
-  Time Frame
This involves concepts related to the passage of time, such as hours, minutes, schedules, deadlines, etc.
-  Money Frame
This involves concepts related to financial transactions, value, budgeting, saving, spending, etc.

Step 2: Analyze input spaces
Time: The source frame includes elements like seconds, hours, schedules, deadlines, etc.
Money: The target frame includes elements like currency, investment, expenses, profit, loss, etc.

Step 3: Analyze Cross-Space Mapping
The elements of the "time" frame are mapped onto the "money" frame. 
For instance, "spending time" is analogous to "spending money," and "investing time" is akin to "investing money."

Step 4: Blended Space
In the blended space, time is conceptualized as a valuable commodity that can be budgeted, spent wisely, or wasted, similar to how money is managed.

Step 5: Emergent Structure
This blend creates a new understanding where activities are seen through the lens of financial transactions. 
For example, "wasting time" implies a loss similar to wasting money, highlighting the value and scarcity of time.

Step 6: Generate sentence
"Time is money."
'''
    prompt = '''Select the relevant FrameNet frames for the following words and generate a frame blending example.
Words: color, time'''
    full_prompt = f"{cot_example}\nUser: {prompt}\nAssistant:"
    response = query_engine.query(full_prompt)
    print(">>> full_prompt")
    print(full_prompt)
    print(">>> response")
    print(response)
    return

if __name__ == "__main__":
    cot()
