import json
import pickle

def load_pickle_file(file_path):
    try:
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        print(f"Error loading pickle file {file_path}: {e}")
        return None

def save_pickle_file(data, file_path):
    try:
        with open(file_path, 'wb') as f:
            pickle.dump(data, f)
    except Exception as e:
        print(f"Error saving pickle file {file_path}: {e}")

def save_json_file(data, file_path):
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error saving JSON file {file_path}: {e}")

def update_goal_set(goal_set, updated_test_set):
    for i, item in enumerate(goal_set['test']):
        if i < len(updated_test_set):
            updated_item = updated_test_set[i]
            item['goal']['explicit_inform_slots'] = updated_item['exp_sxs']
            item['goal']['implicit_inform_slots'] = updated_item['imp_sxs']
    return goal_set

def main():
    goal_set_p_file = 'goal_set.p'
    updated_test_set_file = 'json'
    goal_set_json_file = 'goal_set.json'
    updated_goal_set_p_file = 'updated_goal_set.p'

    goal_set = load_pickle_file(goal_set_p_file)
    if goal_set is None:
        return

    save_json_file(goal_set, goal_set_json_file)

    try:
        with open(updated_test_set_file, 'r', encoding='utf-8') as f:
            updated_test_set = json.load(f)
    except Exception as e:
        print(f"Error loading JSON file {updated_test_set_file}: {e}")
        return

    updated_goal_set = update_goal_set(goal_set, updated_test_set)

    save_pickle_file(updated_goal_set, updated_goal_set_p_file)

if __name__ == "__main__":
    main()
