from rag import get_query_engine, generate_response, cot_multi_conversation
from frame_hierarchy_analyzer import get_frames, analyze_hierarchy

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

prompt = '''Explain how the "Revenge" frame inherits from the "Rewards_and_punishments" frame. Create a frame blending example demonstrating this relationship.'''

cot_prompts = [
    '''Define the "Revenge" frame.''',
    '''Define the "Rewards_and_punishments" frame.''',
    '''Describe how the "Revenge" frame derives its structure and elements from the "Rewards_and_punishments" frame.''',
    '''Develop a scenario that demonstrates how the "Revenge" frame inherits and utilizes aspects of the "Rewards_and_punishments" frame.''',
    '''Explain the input space, cross-space mapping, blended space, and emergent structure.'''
]

test_prompt_cot = '''Let's break down the task into smaller, logical steps to ensure clarity and thoroughness.

1. Define the "Revenge" frame.
2. Define the "Rewards_and_punishments" frame.
3. Explain how the "Revenge" frame derives its structure and elements from the "Rewards_and_punishments" frame.
4. Develop a scenario that demonstrates how the "Revenge" frame inherits and utilizes aspects of the "Rewards_and_punishments" frame. Explain the input space, cross-space mapping, blended space, and emergent structure.

Please follow these steps to provide a detailed and clear explanation.
'''

test_prompt_zero_shot = '''Explain how the "Revenge" frame inherits from the "Rewards_and_punishments" frame. Create a frame blending example demonstrating this relationship.
'''

test_prompt_one_shot = '''Explain how the "Revenge" frame inherits from the "Rewards_and_punishments" frame. For example, the "Revenge" frame involves an Avenger and an Offender, where the Avenger seeks to punish the Offender for a perceived wrong. This is a specific instance of the broader "Rewards_and_punishments" frame, where actions lead to rewards or punishments. Develop a scenario demonstrating this relationship, including input space, cross-space mapping, blended space, and emergent structure. 

For instance, consider a student who seeks revenge on a classmate by reporting them for cheating. The "Revenge" frame maps onto the "Rewards_and_punishments" frame as follows: the student (Avenger) maps to the Punisher, the classmate (Offender) maps to the Punished, and reporting (revenge act) maps to the punishment. This scenario blends personal motives with institutional consequences.
'''

test_prompt_few_shot = '''Explain how the "Revenge" frame inherits from the "Rewards_and_punishments" frame. Create a frame blending example demonstrating this relationship. Here are a few examples to guide you:

1. Example 1:
	- **Revenge Frame:** An employee sabotages a colleague's work as revenge for a past grievance.
	- **Rewards_and_punishments Frame:** Workplace rules where actions (like sabotage) lead to consequences (punishment).
	- **Blending:** The employee (Avenger) maps to the Punisher, the colleague (Offender) maps to the Punished, and sabotage maps to the punishment.

2. Example 2:
	- **Revenge Frame:** A person spreads rumors about a former friend who betrayed them.
	- **Rewards_and_punishments Frame:** Social dynamics where spreading rumors leads to social ostracism.
	- **Blending:** The person (Avenger) maps to the Punisher, the former friend (Offender) maps to the Punished, and rumor-spreading maps to the punishment.

Using these examples as a guide, please explain the inheritance relationship and create a new scenario demonstrating the frame blending.
'''

def cot_prompt(frame1, frame2):
    prompt = f'''Let's break down the task into smaller, logical steps to ensure clarity and thoroughness.

1. Define the "{frame1}" frame.
2. Define the "{frame2}" frame.
3. Explain how the "{frame1}" frame can have cross-space mapping with "{frame2}" frame on their structures and elements.
4. Develop a sentence and scenario that demonstrates how the "{frame1}" frame blends with "{frame2}" frame. Prefer to use rhetorical devices such as Analogy and Metaphor. Explain the input space, cross-space mapping, blended space, and emergent structure.

Please follow these steps to provide a detailed and clear explanation.
'''
    return prompt

def prompt_close_to(frame):
    return f"What frames are close to '{frame}'?"

def prompt_zero_shot_blending(frame1, frame2):
    return f"""Create a frame blending example between "{frame1}" frame and "{frame2}" frame. Prefer to use rhetorical devices such as Analogy and Metaphor."""

if __name__ == "__main__":
    query_engine = get_query_engine()
    response = generate_response(query_engine, prompt_zero_shot_blending("Political_locales", "Birth_scenario"))
    # response = generate_response(query_engine, prompt_close_to("murder"))
    # print(response.frame_names)
    # print(', '.join(response.frame_names))
    # root = analyze_hierarchy(get_frames("frame_json"), "Inheritance")
    # for frame in response.frame_names:
    #     if root.find(frame):
    #         print(root.find(frame))

