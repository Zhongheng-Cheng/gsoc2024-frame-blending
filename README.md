# gsoc2024-frame-blending

## Overview

This [Google Summer of Code (GSoC)](https://summerofcode.withgoogle.com/) 2024 project "Frame Blending by LLMs" is contributed by [Zhongheng Cheng](https://github.com/Zhongheng-Cheng) with [Red Hen Lab](https://www.redhenlab.org/home).

My personal progress blog can be found [here](https://zhongheng-cheng.github.io/)

## Table of Contents

- [Installation](#installation)
- [Frame Hierarchy Analysis](#frame-hierarchy-analysis)
- [FrameNet XML Parser](#framenet-xml-parser)
- [RAG for Llama2 (Huggingface)](#rag-for-llama2-huggingface)
- [Llama2 (Meta)](#llama2-meta)

## Installation

Follow the instructions to setup environment.

Modules to load on CWRU HPC:
- Python/3.11.3
- PyTorch/2.1.2-foss-2023a-CUDA-12.1.1
- PyYAML/6.0-GCCcore-12.3.0

```bash
# Cloning the repository
git clone https://github.com/Zhongheng-Cheng/gsoc2024-frame-blending
cd gsoc2024-frame-blending

# [Optional] Creating virtual environment
python -m venv venv
source venv/bin/activate

# Download dependencies
pip install -r requirements.txt

# Setup Huggingface API key
touch .env
# Enter your Huggingface API key in ".env" like this:
# HUGGINGFACE_API_KEY="..."
```

## Frame Hierarchy Analysis

## FrameNet XML Parser

## RAG for Llama2 (Huggingface)

## Llama2 (Meta)

Referring to [Meta - 5 Steps to Getting Started with Llama 2](https://ai.meta.com/blog/5-steps-to-getting-started-with-llama-2/)

0. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate   # enter the virtual environment
```
1. Download dependencies
```bash
pip install -r requirements.txt
```
2. Download the model 

Request download access to Llama 2 [here](https://llama.meta.com/llama-downloads)

```bash
git clone https://github.com/facebookresearch/llama
cd llama
./download.sh # requires the pre-signed URL from Meta License
```
3. Convert the model weights to run with Hugging Face
```bash
# in the llama/ directory

# create a link to the tokenizer
ln -h ./tokenizer.model ./llama-2-7b-chat/tokenizer.model

# convert to hugging face format
TRANSFORM=`python -c "import transformers;print('/'.join(transformers.__file__.split('/')[:-1])+'/models/llama/convert_llama_weights_to_hf.py')"`
pip install protobuf && python $TRANSFORM --input_dir ./llama-2-7b-chat --model_size 7B --output_dir ./llama-2-7b-chat-hf
```
4. Write Python scripts and run the model
```bash
python main.py
```
