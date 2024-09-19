import json
import os
import argparse

def merge_symptoms(item):
    symptoms = {}
    symptoms.update(item.get('implicit_inform_slots', {}))
    symptoms.update(item.get('explicit_inform_slots', {}))
    return symptoms

def process_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    processed_data = []
    for item in data:
        dialog = item.get("dialog", [])
        disease_tag = item.get("disease_tag", "")
        goal = item.get("goal", {})

        symptoms = merge_symptoms(item)

        new_item = {
            "dialog": dialog,
            "disease_tag": disease_tag,
            "symptom": symptoms
        }
        processed_data.append(new_item)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(processed_data, f, ensure_ascii=False, indent=4)

def main():
    parser = argparse.ArgumentParser(description="Process JSON files in a specified dataset folder.")
    parser.add_argument('--dataset', type=str, required=True, help="The dataset folder containing the JSON files.")

    args = parser.parse_args()
    dataset_folder = args.dataset

    file_pairs = [('ori_train.json', 'train.json'), ('ori_test.json', 'test.json')]

    for input_file, output_file in file_pairs:
        input_path = os.path.join(dataset_folder, input_file)
        output_path = os.path.join(dataset_folder, output_file)
        process_file(input_path, output_path)

if __name__ == '__main__':
    main()
