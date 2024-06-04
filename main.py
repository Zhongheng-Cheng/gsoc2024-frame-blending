from transformers import AutoModelForCausalLM, AutoTokenizer

# Load the model and tokenizer
model_name = "NousResearch/Llama-2-7b-chat-hf"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Tokenize input
input_text = "Hello, how are you?"
inputs = tokenizer(input_text, return_tensors="pt")

# Generate response
output = model.generate(**inputs, max_length=100)
response = tokenizer.decode(output[0], skip_special_tokens=True)

print(response)
