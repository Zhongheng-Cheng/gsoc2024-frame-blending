import torch
import transformers

from transformers import LlamaForCausalLM, LlamaTokenizer

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

def generate_result(prompt):
    sequences = pipeline(
        prompt,
        do_sample=True,
        top_k=10,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id,
        max_length=400,
    )
    return sequences

while True:
    prompt = input(">>> Prompt: ")
    sequences = generate_result(prompt + "\n")
    print(sequences)

    for seq in sequences:
        print(f"{seq['generated_text']}")
