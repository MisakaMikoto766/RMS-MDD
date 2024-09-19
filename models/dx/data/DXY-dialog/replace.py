import json


def load_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_symptoms_file(file_path):
    symptoms = []
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("患者症状:"):
                symptoms_part = line.split("患者症状:")[1].strip()
                symptoms_list = symptoms_part.split(',')
                symptom_dict = {}
                for symptom in symptoms_list:
                    symptom_name, status = symptom.split(':')
                    symptom_dict[symptom_name] = "1" if status == "True" else "0"
                symptoms.append(symptom_dict)
    return symptoms


def process_and_save(train_set_file, dialog_file, selfrepo_file, output_file):
    train_set = load_json_file(train_set_file)
    dialog_symptoms = load_symptoms_file(dialog_file)
    selfrepo_symptoms = load_symptoms_file(selfrepo_file)

    assert len(train_set) == len(dialog_symptoms) == len(selfrepo_symptoms), "False"

    for i in range(len(train_set)):
        train_set[i]['exp_sxs'] = selfrepo_symptoms[i]
        train_set[i]['imp_sxs'] = dialog_symptoms[i]

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(train_set, f, ensure_ascii=False, indent=4)

def main():
    train_set_file = 'test_set.json'
    dialog_file = 'dialog.txt'
    selfrepo_file = 'selfrepo.txt'
    output_file = 'test_set_up.json'

    process_and_save(train_set_file, dialog_file, selfrepo_file, output_file)


if __name__ == "__main__":
    main()
