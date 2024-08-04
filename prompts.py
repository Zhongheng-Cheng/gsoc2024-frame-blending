class Prompts:

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

    rhetorical = """Prefer to use rhetorical devices such as Analogy and Metaphor."""

    def zero_shot_blending(self, frames: list[str] = [], rhetorical: bool = True):
        prompt = f"""Create a frame blending example sentence between frames: "{'", "'.join(frames)}". """
        if rhetorical:
            prompt += '\n' + self.rhetorical
        return prompt

    def one_shot_blending(self, frames: list[str] = [], rhetorical: bool = True):
        return self.zero_shot_blending(frames, rhetorical) + '\n' + self.one_shot_example

    def cot_blending(self, frames: list[str] = [], rhetorical: bool = True):
        n = len(frames)
        prompt = f'''Let's break down the task into smaller, logical steps to ensure clarity and thoroughness.

{'\n'.join([f"{i + 1}. Define the '{frame}' frame." for i, frame in enumerate(frames)])}
{n + 1}. Explain how these frames can have cross-space mapping on their structures and elements.
{n + 2}. Create a frame blending example sentence that demonstrates how these frames blend. Explain the input space, cross-space mapping, blended space, and emergent structure.

Please follow these steps to provide a detailed and clear explanation.
'''
        if rhetorical:
            prompt += '\n' + self.rhetorical
        return prompt

    def frame_close_to(self, frame):
        return f"What frames are close to '{frame}'?"


if __name__ == "__main__":
    # from rag import get_query_engine, generate_response
    # from frame_hierarchy_analyzer import get_frames, analyze_hierarchy
    # query_engine = get_query_engine()
    # response = generate_response(query_engine, prompt_zero_shot_blending("Political_locales", "Birth_scenario"))
    prompts = Prompts()
    frames = ["Travel", "Aging", "Aaa", "Bbb"]
    prompt = prompts.zero_shot_blending(frames)
    print(prompt)
    print()
    prompt = prompts.one_shot_blending(frames)
    print(prompt)
    print()
    prompt = prompts.cot_blending(frames)
    print(prompt)

