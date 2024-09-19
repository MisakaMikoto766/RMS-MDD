import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig
import jsonlines
import os
import argparse
from tqdm import tqdm
from dx.utils import extract_pairs

tokenizer = AutoTokenizer.from_pretrained("/mnt/HuatuoGPT2-7B/", use_fast=True, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained("/mnt/HuatuoGPT2-7B/", device_map="auto", torch_dtype='auto',
                                             trust_remote_code=True)


def process_symptoms_from_file(input_file_path, output_file_path, history_template, max_output_length=96):
    generation_config = GenerationConfig(max_new_tokens=max_output_length)
    with jsonlines.open(input_file_path) as reader, open(output_file_path, 'w', encoding='utf-8') as output_file:
        for item in tqdm(reader, desc="Processing"):
            query = item.get('query')
            history = history_template.copy()
            history.append({"role": "user", "content": query})
            res = model.HuatuoChat(tokenizer, history, generation_config=generation_config)
            output_file.write(f"{res}\n")
            history.pop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process symptoms from a dataset file.")
    parser.add_argument('--dataset_file', type=str, required=True, help='Name of the dataset folder in ../data/.')
    parser.add_argument('--output_file', type=str, required=True, help='Name of the output file to store results.')

    args = parser.parse_args()

    input_file_path = os.path.join("..", "data", args.dataset_file, "test_pre.jsonl")
    output_dir = os.path.join("..", "output", args.dataset_file)
    os.makedirs(output_dir, exist_ok=True)

    output_file_path = os.path.join(output_dir, args.output_file)

    training_file_path = os.path.join("..", "data", args.dataset_file, "train_pre.jsonl")

    extracted_prompts, extracted_results = extract_pairs(training_file_path, num_samples=3)

    history_template = [
        {"role": "system", "content": "prompt"},
        # (query1,answer1)
        {"role": "user", "content": extracted_prompts[0]},
        {"role": "assistant", "content": extracted_results[0]},
        # (query2,answer2)
        {"role": "user", "content": extracted_prompts[1]},
        {"role": "assistant", "content": extracted_results[1]},
        # (query3,answer3)
        {"role": "user", "content": extracted_prompts[2]},
        {"role": "assistant", "content": extracted_results[2]},
    ]

    process_symptoms_from_file(input_file_path, output_file_path, history_template)
