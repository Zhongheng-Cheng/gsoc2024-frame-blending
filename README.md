# gsoc2024-frame-blending

## Downloading and installation of Llama 2

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
