def llama2_llamaindex():
    from torch import float16
    from llama_index.llms.huggingface import HuggingFaceLLM
    from llama_index.core import PromptTemplate

    LLAMA2_7B = "meta-llama/Llama-2-7b-hf"
    LLAMA2_7B_CHAT = "meta-llama/Llama-2-7b-chat-hf"
    LLAMA2_13B = "meta-llama/Llama-2-13b-hf"
    LLAMA2_13B_CHAT = "meta-llama/Llama-2-13b-chat-hf"
    LLAMA2_70B = "meta-llama/Llama-2-70b-hf"
    LLAMA2_70B_CHAT = "meta-llama/Llama-2-70b-chat-hf"

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

    return HuggingFaceLLM(
        context_window=4096,
        max_new_tokens=2048,
        generate_kwargs={"temperature": 0.9, "do_sample": True},
        query_wrapper_prompt=query_wrapper_prompt,
        tokenizer_name=LLAMA2_7B_CHAT,
        model_name=LLAMA2_7B_CHAT,
        device_map="auto",
        # change these settings below depending on your GPU
        model_kwargs={"torch_dtype": float16, "load_in_8bit": True},
    )

def llama2_ollama():
    from llama_index.llms.ollama import Ollama

    # llama2 refers to llama2-7b-chat
    return Ollama(model="llama2", request_timeout=600.0)

def embed_model():
    from llama_index.embeddings.huggingface import HuggingFaceEmbedding

    return HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
