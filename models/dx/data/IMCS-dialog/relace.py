import json

def load_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading JSON file {file_path}: {e}")
        return None


import json


def map_status(status):
    if status == "True":
        return "1"
    elif status == "False":
        return "0"
    elif status == "not sure":
        return "2"
    return None

def load_symptoms_file(file_path):
    symptoms = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

            for line in lines:
                if not line.startswith("患者症状:"):
                    continue
                symptoms_part = line.split("患者症状:")[1].strip()
                if not symptoms_part:
                    symptoms.append({})
                    continue

                symptoms_list = symptoms_part.split(',')
                symptom_dict = {}

                for symptom in symptoms_list:
                    try:
                        symptom_name, status = symptom.split(':')
                    except ValueError:
                        print(f"Error parsing symptom: {symptom}")
                        continue

                    mapped_status = map_status(status)
                    if mapped_status is None:
                        continue

                    symptom_dict[symptom_name] = mapped_status

                symptoms.append(symptom_dict)

    except Exception as e:
        print(f"Error reading symptoms file {file_path}: {e}")

    return symptoms


def process_and_save(train_set_file, dialog_file, selfrepo_file, output_file):
    train_set = load_json_file(train_set_file)
    dialog_symptoms = load_symptoms_file(dialog_file)
    selfrepo_symptoms = load_symptoms_file(selfrepo_file)

    if train_set is None or not dialog_symptoms or not selfrepo_symptoms:
        print("Error: One or more files failed to load.")
        return

    if len(train_set) != len(dialog_symptoms) or len(train_set) != len(selfrepo_symptoms):
        print("Error: Sample count mismatch between files.")
        return

    for i in range(len(train_set)):
        train_set[i]['exp_sxs'] = selfrepo_symptoms[i]
        train_set[i]['imp_sxs'] = dialog_symptoms[i]

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(train_set, f, ensure_ascii=False, indent=4)
        print(f"Processing completed. Output saved to {output_file}.")
    except Exception as e:
        print(f"Error saving output file {output_file}: {e}")

def main():
    train_set_file = 'test_set.json'
    dialog_file = 'dialog.txt'
    selfrepo_file = 'selfrepo.txt'
    output_file = 'test_set_up.json'

    process_and_save(train_set_file, dialog_file, selfrepo_file, output_file)

if __name__ == "__main__":
    main()
