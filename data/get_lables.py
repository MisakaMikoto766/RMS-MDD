import json
import os
import argparse

def extract_data_from_file(file_path):
    diseases = set()
    symptoms = set()

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

        for entry in data:
            diseases.add(entry.get('disease_tag', '').strip())
            symptom_dict = entry.get('symptom', {})
            for symptom in symptom_dict:
                symptoms.add(symptom.strip())

    return diseases, symptoms

def save_to_file(items, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in sorted(items):
            f.write(f"{item}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process disease and symptom data.")
    parser.add_argument('--dataset_dir', type=str, required=True, help='Path to the dataset directory')

    args = parser.parse_args()
    dataset_dir = args.dataset_dir

    train_file = os.path.join(dataset_dir, "train.json")
    test_file = os.path.join(dataset_dir, "test.json")

    train_diseases, train_symptoms = extract_data_from_file(train_file)
    test_diseases, test_symptoms = extract_data_from_file(test_file)

    all_diseases = train_diseases.union(test_diseases)
    all_symptoms = train_symptoms.union(test_symptoms)

    disease_output_file = os.path.join(dataset_dir, "standard_disease.txt")
    symptom_output_file = os.path.join(dataset_dir, "standard_symptom.txt")

    save_to_file(all_diseases, disease_output_file)
    save_to_file(all_symptoms, symptom_output_file)

    print(f"Disease and symptom extraction completed and saved to {dataset_dir}.")
