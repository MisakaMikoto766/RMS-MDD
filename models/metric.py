import json
import re
import random
import argparse
import os

parser = argparse.ArgumentParser(description="Evaluate LLM predictions")
parser.add_argument('--dataset', type=str, required=True, help='Dataset name')
args = parser.parse_args()

dataset = args.dataset
file_path = f'../output/{dataset}/final.txt'
test_json_path = f'../data/{dataset}/test.json'

with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read()

content = re.sub(r'\(.*?\)|（.*?）', '', content)
content = content.replace('， ', ',')
content = content.replace('：', ':')
content = content.replace('。', '.')

with open(file_path, 'w', encoding='utf-8') as file:
    file.write(content)

with open(test_json_path, 'r', encoding='utf-8') as f:
    test_data = json.load(f)

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

predictions = content.strip().split('\n')

possible_statuses = [True, False, 'not sure']

status_mapping = {
    "True": True,
    "False": False,
    "true": True,
    "false": False,
    "not sure": 'not sure'
}

def parse_prediction(pred, previous_disease=None):
    pred = pred.strip()
    symptoms = {}
    if 'The patient\'s symptoms:' in pred and 'The patient\'s disease:' in pred:
        symptoms_part, disease_part = pred.split('The patient\'s disease:')
        symptoms_part = symptoms_part.replace('The patient\'s symptoms:', '').strip()
        disease = disease_part.strip().strip('.').replace('，', '')
        seen = set()
        for sym in symptoms_part.split(","):
            if ':' in sym:
                key, value = sym.split(":")
                if key not in seen:
                    symptoms[key.strip()] = status_mapping.get(value.strip(), random.choice(possible_statuses))
                    seen.add(key.strip())
        return symptoms, disease
    return None, None

ground_truths = [(entry["symptom"], entry["disease_tag"]) for entry in test_data]

predicted_values = []
previous_disease = None
for pred in predictions:
    symptoms, disease = parse_prediction(pred, previous_disease)
    if disease:
        previous_disease = disease
    predicted_values.append((symptoms, disease))

all_true_positives = 0
all_total_predicted = 0
all_total_actual = 0

correct_disease_predictions = 0
total_disease_predictions = len(ground_truths)

strict_match_count = 0
symptom_match_score_sum = 0

for (true_symptoms, true_disease), (pred_symptoms, pred_disease) in zip(ground_truths, predicted_values):
    true_positives = sum(1 for symptom, value in true_symptoms.items() if pred_symptoms.get(symptom) == value)
    total_predicted = len(pred_symptoms)
    total_actual = len(true_symptoms)

    all_true_positives += true_positives
    all_total_predicted += total_predicted
    all_total_actual += total_actual

    if true_disease == pred_disease:
        correct_disease_predictions += 1

    if true_disease == pred_disease and set(true_symptoms.items()) == set(pred_symptoms.items()):
        strict_match_count += 1

    if true_disease == pred_disease:
        symptom_match_score_sum += true_positives / total_actual if total_actual > 0 else 0
    else:
        symptom_match_score_sum += (true_positives * 0.5) / total_actual if total_actual > 0 else 0

precision = all_true_positives / all_total_predicted if all_total_predicted else 0
recall = all_true_positives / all_total_actual if all_total_actual else 0
f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) else 0

disease_accuracy = correct_disease_predictions / total_disease_predictions if total_disease_predictions else 0
strict_match_accuracy = strict_match_count / total_disease_predictions if total_disease_predictions else 0

symptom_match_score = symptom_match_score_sum / total_disease_predictions if total_disease_predictions else 0

print(f'P: {precision:.4f}')
print(f'R: {recall:.4f}')
print(f'F1: {f1:.4f}')
print(f'ACC: {disease_accuracy:.4f}')
print(f'Csdm: {strict_match_accuracy:.4f}')
print(f'Sdm: {symptom_match_score:.4f}')
