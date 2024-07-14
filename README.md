# gsoc2024-frame-blending

## Overview

This [Google Summer of Code (GSoC)](https://summerofcode.withgoogle.com/) 2024 project "Frame Blending by LLMs" is contributed by [Zhongheng Cheng](https://github.com/Zhongheng-Cheng) with [Red Hen Lab](https://www.redhenlab.org/home).

My personal progress blog can be found [here](https://zhongheng-cheng.github.io/)

## Table of Contents

- [Installation](#installation)
- [Frame Hierarchy Analyzer](#frame-hierarchy-analyzer)
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

## Frame Hierarchy Analyzer

### Introduction

This section of the project focuses on analyzing linguistic frame hierarchies. It involves constructing a tree-like structure to represent frame relations, searching within this structure, and performing other relevant analyses.

### Usage

```python
from frame_hierarchy_analyzer import analyze_hierarchy, save_hierarchy_to_file

# Example of building a hierarchy
frames = ['Event', 'Action', ...]
frame_relation = 'Inheritance'
reverse_order = False # False: In direction of "Is Inherited by"; True: In direction of "Inherits from"
root = analyze_hierarchy(frames, frame_relation, reverse_order) # Returns the root node of the tree hierarchy

# Finding a specific frame node
node = root.find('Event')

# Print the visualized hierarchy of any node with its subnodes
print(node)

# Counts the total number of nodes in the subtree including this node
total_number = node.count()

# Get the list of immediate child nodes of this node
children = node.children()

# Saving the hierarchy to a file
save_hierarchy_to_file(root, 'output_hierarchy.txt')
```

## FrameNet XML Parser

### Introduction

This code transforms the original FrameNet data in XML format to JSON format, leaving out unimportant information for frame analysis, such as frame ID and created data. Mainly developed by [Rohan](https://medium.com/@rohank587/spending-the-summer-24-in-gsoc-with-red-hen-lab-5c8aade49026). Minor modifications are made to accommodate the FrameNet data input in JSON format for [Frame Hierarchy Analyzer](#frame-hierarchy-analyzer).

### Usage

```python
from framenet_xml_parser import parse

# Example of parsing a directory of .xml files
xml_folder_path = "frame"
json_folder_path = "frame_json"
parse(xml_folder_path, json_folder_path)
```

## RAG for Llama2 (Huggingface)

### Introduction

This code utilizes Llama2-7b-chat with Huggingface API, and achieves Retrieval Augmented Generation (RAG) leveraging Llama-index. Specifically, a JSON parser is used to read all the JSON-format FrameNet frame data, and create a query engine with vector store index for querying.

When using `get_query_engine()`, the index created upon reading data files would be saved to `./query_engine.index/`, and be automatically loaded when getting query engine next time. To avoid saving index data locally, you can specify `save_index=False` as a parameter for `get_query_engine()`.

### Usage

```python
from rag import get_query_engine, generate_response

prompt = "..."
query_engine = get_query_engine()
response = generate_response(query_engine, prompt)
```

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
