import json
import argparse
import os
import random
from typing import Any
from llama_index.core import Settings
from llama_index.core.base.llms.types import LLMMetadata, CompletionResponse, CompletionResponseGen
from llama_index.core.llms import CustomLLM
from llama_index.core.llms.callbacks import llm_completion_callback
from swift.llm import get_model_list_client, XRequestConfig, inference_client
from dx.utils import extract_pairs


# Reference:
query1 = "query1"
answer1 = "answer1"
query2 = "query2"
answer2 = "answer2"
query3 = "query3"
answer3 = "answer3"

model_list = get_model_list_client()
model_type = model_list.data[0].id
request_config = XRequestConfig(stream=True)

class RMSLLM(CustomLLM):
    context_window: int = 4096
    num_output: int = 2048
    model_name: str = "RMS-MDD"

    @property
    def metadata(self) -> LLMMetadata:
        return LLMMetadata(
            context_window=self.context_window,
            num_output=self.num_output,
            model_name=self.model_name,
        )

    @llm_completion_callback()
    def complete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        final_text = ""
        # Reference:
        # stream_resp = inference_client(model_type, prompt, [(query1, answer1), (query2, answer2), (query3, answer3)],
        #                                system=SYSTEM_PROMPT, request_config=request_config)
        stream_resp = inference_client(model_type, prompt, system=SYSTEM_PROMPT, request_config=request_config)
        for chunk in stream_resp:
            final_text += chunk.choices[0].delta.content
        return CompletionResponse(text=final_text)

    @llm_completion_callback()
    def stream_complete(self, prompt: str, **kwargs: Any) -> CompletionResponseGen:
        resp = inference_client(model_type, prompt, [()], request_config=request_config)
        response = ""
        for token in resp.choices[0].message.content:
            response += token
            yield CompletionResponse(text=response, delta=token)

Settings.llm = RMSLLM()

SYSTEM_PROMPT = """You are an experienced medical diagnostic doctor..."""

def process_symptoms_from_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f, open(output_file, 'w', encoding='utf-8') as output:
        for line in f:
            item = json.loads(line)
            cr_query = item.get('query')

            llm = RMSLLM()
            response = llm.complete(cr_query)
            output.write(f"{response.text}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process symptoms from a dataset file.")
    parser.add_argument('--dataset_file', type=str, required=True, help='Name of the dataset folder in ../data/.')
    parser.add_argument('--output_file', type=str, required=True, help='Name of the output file to store results.')

    args = parser.parse_args()

    input_file = os.path.join("..", "data", args.dataset_file, "test_pre.jsonl")
    output_dir = os.path.join("..", "output", args.dataset_file)
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, args.output_file)

    training_file_path = os.path.join("..", "data", args.dataset_file, "train_pre.jsonl")
    extracted_prompts, extracted_results = extract_pairs(training_file_path, sample_count=3)
    sample_query1, sample_query2, sample_query3 = extracted_prompts
    sample_answer1, sample_answer2, sample_answer3 = extracted_results

    process_symptoms_from_file(input_file, output_file)
