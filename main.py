import torch
import transformers

from transformers import LlamaForCausalLM, LlamaTokenizer
import time

def generate_result(prompt):
    sequences = pipeline(
        prompt,
        do_sample=True,
        top_k=10,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id,
        max_length=800,
    )
    return sequences

def keep_asking():
    while True:
        prompt = input(">>> Prompt: ")
        sequences = generate_result(prompt + "\n")
        for seq in sequences:
            print(f"{seq['generated_text']}")

def ask_once(prompt):
    start_time = time.time()
    sequences = generate_result(prompt + "\n")
    for seq in sequences:
        print(f"{seq['generated_text']}")
    print(f"Result generating finished, elapsed time: {time.time() - start_time:.2f}s")

if __name__ == "__main__":
    model_dir = "./llama/llama-2-7b-chat-hf"
    model = LlamaForCausalLM.from_pretrained(model_dir)
    tokenizer = LlamaTokenizer.from_pretrained(model_dir)

    pipeline = transformers.pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        torch_dtype=torch.float16,
        device_map="auto",
    )

    prompt = '''Here is an example of frame blending: 
    Expression: "Time is money."
    Frames Involved:
    Time Frame: This involves concepts related to the passage of time, such as hours, minutes, schedules, deadlines, etc.
    Money Frame: This involves concepts related to financial transactions, value, budgeting, saving, spending, etc.
    Analysis of the Frame Blending
    Input Spaces:
    Time: The source frame includes elements like seconds, hours, schedules, deadlines, etc.
    Money: The target frame includes elements like currency, investment, expenses, profit, loss, etc.
    Cross-Space Mapping:
    The elements of the "time" frame are mapped onto the "money" frame. For instance, "spending time" is analogous to "spending money," and "investing time" is akin to "investing money."
    Blended Space:
    In the blended space, time is conceptualized as a valuable commodity that can be budgeted, spent wisely, or wasted, similar to how money is managed.
    Emergent Structure:
    This blend creates a new understanding where activities are seen through the lens of financial transactions. For example, "wasting time" implies a loss similar to wasting money, highlighting the value and scarcity of time.
    Give me another example of frame blending based on the example I gave you.'''
    ask_once(prompt)