import json
import os
import argparse

def process_json_file(input_filename, output_filename):
    with open(input_filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    with open(output_filename, 'w', encoding='utf-8') as f:
        for item in data:
            # ========== Processing conversation data ==========
            dialog_list = item.get('dialog', [])

            # Get disease labels
            disease_tag = item.get('disease_tag', '无')
            # disease_tag = item.get('disease_tag', 'None')

            # Filter out conversations containing disease tags
            filtered_dialog = [dialog for dialog in dialog_list if disease_tag not in dialog]

            formatted_dialog = '\n'.join([dialog.strip() for dialog in filtered_dialog])

            symptoms = item.get('symptom', {})
            symptoms_desc = [f"{symptom}:{status}" for symptom, status in symptoms.items()]
            all_symptoms_desc = ', '.join(symptoms_desc) if symptoms_desc else '无'
            # all_symptoms_desc = ', '.join(symptoms_desc) if symptoms_desc else 'None'

            # ========== Constructing query and response ==========

            # prompt
            query = f"对话：{formatted_dialog}"
            response = f"患者症状:{all_symptoms_desc}, 患者疾病:{disease_tag}。"

            lora_entry = json.dumps({"query": query, "response": response}, ensure_ascii=False)
            f.write(lora_entry + '\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Processing JSON files of different datasets')
    parser.add_argument('--dataset', type=str, required=True, help='Dataset folder name')

    args = parser.parse_args()

    # Process test.json
    input_test_filename = os.path.join(args.dataset, 'test.json')
    output_test_filename = os.path.join(args.dataset, 'test_pre.jsonl')
    process_json_file(input_test_filename, output_test_filename)

    # Process train.json
    input_train_filename = os.path.join(args.dataset, 'train.json')
    output_train_filename = os.path.join(args.dataset, 'train_pre.jsonl')
    process_json_file(input_train_filename, output_train_filename)

