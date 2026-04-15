from itertools import product
import re
import string
import json
import networkx as nx


digitMap = {
    'none': '0',
    'zero': '0',
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
    'ten': '10',
    'entailment': 'yes',
    'true': 'yes',
    'contradiction': 'no',
    'false': 'no',
}


contractions = {
    'aint': "ain't",
    'arent': "aren't",
    'cant': "can't",
    'couldve': "could've",
    'couldnt': "couldn't",
    "couldn'tve": "couldn't've",
    "couldnt've": "couldn't've",
    'didnt': "didn't",
    'doesnt': "doesn't",
    'dont': "don't",
    'hadnt': "hadn't",
    "hadnt've": "hadn't've",
    "hadn'tve": "hadn't've",
    'hasnt': "hasn't",
    'havent': "haven't",
    'hed': "he'd",
    "hed've": "he'd've",
    "he'dve": "he'd've",
    'hes': "he's",
    'howd': "how'd",
    'howll': "how'll",
    'hows': "how's",
    "Id've": "I'd've",
    "I'dve": "I'd've",
    'Im': "I'm",
    'Ive': "I've",
    'isnt': "isn't",
    'itd': "it'd",
    "itd've": "it'd've",
    "it'dve": "it'd've",
    'itll': "it'll",
    "let's": "let's",
    'maam': "ma'am",
    'mightnt': "mightn't",
    "mightnt've": "mightn't've",
    "mightn'tve": "mightn't've",
    'mightve': "might've",
    'mustnt': "mustn't",
    'mustve': "must've",
    'neednt': "needn't",
    'notve': "not've",
    'oclock': "o'clock",
    'oughtnt': "oughtn't",
    "ow's'at": "'ow's'at",
    "'ows'at": "'ow's'at",
    "'ow'sat": "'ow's'at",
    'shant': "shan't",
    "shed've": "she'd've",
    "she'dve": "she'd've",
    "she's": "she's",
    'shouldve': "should've",
    'shouldnt': "shouldn't",
    "shouldnt've": "shouldn't've",
    "shouldn'tve": "shouldn't've",
    "somebody'd": 'somebodyd',
    "somebodyd've": "somebody'd've",
    "somebody'dve": "somebody'd've",
    'somebodyll': "somebody'll",
    'somebodys': "somebody's",
    'someoned': "someone'd",
    "someoned've": "someone'd've",
    "someone'dve": "someone'd've",
    'someonell': "someone'll",
    'someones': "someone's",
    'somethingd': "something'd",
    "somethingd've": "something'd've",
    "something'dve": "something'd've",
    'somethingll': "something'll",
    'thats': "that's",
    'thered': "there'd",
    "thered've": "there'd've",
    "there'dve": "there'd've",
    'therere': "there're",
    'theres': "there's",
    'theyd': "they'd",
    "theyd've": "they'd've",
    "they'dve": "they'd've",
    'theyll': "they'll",
    'theyre': "they're",
    'theyve': "they've",
    'twas': "'twas",
    'wasnt': "wasn't",
    "wed've": "we'd've",
    "we'dve": "we'd've",
    'weve': "we've",
    'werent': "weren't",
    'whatll': "what'll",
    'whatre': "what're",
    'whats': "what's",
    'whatve': "what've",
    'whens': "when's",
    'whered': "where'd",
    'wheres': "where's",
    'whereve': "where've",
    'whod': "who'd",
    "whod've": "who'd've",
    "who'dve": "who'd've",
    'wholl': "who'll",
    'whos': "who's",
    'whove': "who've",
    'whyll': "why'll",
    'whyre': "why're",
    'whys': "why's",
    'wont': "won't",
    'wouldve': "would've",
    'wouldnt': "wouldn't",
    "wouldnt've": "wouldn't've",
    "wouldn'tve": "wouldn't've",
    'yall': "y'all",
    "yall'll": "y'all'll",
    "y'allll": "y'all'll",
    "yall'd've": "y'all'd've",
    "y'alld've": "y'all'd've",
    "y'all'dve": "y'all'd've",
    'youd': "you'd",
    "youd've": "you'd've",
    "you'dve": "you'd've",
    'youll': "you'll",
    'youre': "you're",
    'youve': "you've"
}


def max_people_to_accommodate(m, n, keys):
    G = nx.Graph()

    for i in range(m):
        G.add_node(f'person_{i}', bipartite=0)

    for j in range(n):
        G.add_node(f'room_{j}', bipartite=1)

    for i in range(m):
        for room in keys[i]:
            G.add_edge(f'person_{i}', f'room_{room}')

    components = list(nx.connected_components(G))

    accommodated_people = 0

    for component in components:
        subgraph = G.subgraph(component)
        if nx.is_bipartite(subgraph):
            matching = nx.bipartite.maximum_matching(subgraph)
            accommodated_people += sum(1 for person in range(m) if f'person_{person}' in matching)
    
    return accommodated_people


def normalize_answer(text):
    def remove_articles(text):
        return re.sub(r'\b(the answer is|a|an|the)\b', ' ', text)

    def white_space_fix(text):
        return ' '.join(text.split())

    def remove_punctuation(text):
        return ''.join(ch for ch in text if ch not in set(string.punctuation + '‘’´`_'))

    def standarize_digits_and_contractions(text):
        result = []
        text_split = text.split()
        for w in text_split:
            w = digitMap.get(w, w)
            w = contractions.get(w, w)
            result.append(w)
        return ' '.join(result)

    return white_space_fix(standarize_digits_and_contractions(remove_articles(remove_punctuation(text.lower()))))


def convert_to_list(text):
    text = text.strip()
    
    try:
        result = eval(text)
        if isinstance(result, list):
            return result
    except:
        pass
    
    if '[' in text and ']' in text:
        start = text.find('[') + 1
        end = text.find(']')
        content = text[start:end]
        return [item.strip() for item in content.split(',') if item.strip()]
    
    elif '[' in text:
        start = text.find('[') + 1
        content = text[start:]
        return [item.strip() for item in content.split(',') if item.strip()]
    
    elif ']' in text:
        end = text.find(']')
        content = text[:end]
        return [item.strip() for item in content.split(',') if item.strip()]
    
    else:
        return [item.strip() for item in text.split(',') if item.strip()]


def calculate_iou(a_pred, a_eval):
    intersection = len(set(a_pred) & set(a_eval))
    union = len(set(a_pred) | set(a_eval))
    return intersection / union if union != 0 else 0


def evaluate_predictions(a_pred, a_evals):
    if not a_pred:
        return 0.0
    max_score = 0

    a_pred = [normalize_answer(str(ans)) for ans in a_pred]

    a_evals = [[normalize_answer(str(ans)) for ans in eval_set] for eval_set in a_evals]

    a_evals_flattened = set([ans for eval_set in a_evals for ans in eval_set])

    if not (set(a_pred) & a_evals_flattened):
        return 0.0

    keys = []
    m = len(a_pred)
    n = len(a_evals)

    for ans in a_pred:
        indices = []
        for idx, eval_set in enumerate(a_evals):
            if ans in eval_set:
                indices.append(idx)
            if indices:
                keys.append(indices)
    result = min(len(keys), len(set([t for key in keys for t in key ])))
    # result = max_people_to_accommodate(len(keys), n, keys)
    max_score = result / (m + n - result)

    # for a_eval in product(*a_evals):
    #     jaccard_index = calculate_iou(a_pred, a_eval)
    #     max_score = max(max_score, jaccard_index)
    
    return max_score


def read_jsonl_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return [json.loads(line.strip()) for line in f]


def calculate_accuracy(predictions_file):
    predictions = read_jsonl_file(predictions_file)

    total_accuracy = 0
    total_samples = len(predictions)
    question_hop_accuracy = {1: [], 2: [], 3: [], 'greater_than_3': []}
    entity_num_accuracy = {1: [], 2: [], 3: [], 'greater_than_3': []}


    for data in predictions:
        predicted_answers = data['predicted_answers']
        answer_evals = data['answer_evals']
        question_hop = data['question_hop']
        entity_num = data['entity_num']
        
        accuracy = evaluate_predictions(predicted_answers, answer_evals)
        total_accuracy += accuracy
        
        if question_hop == 1:
            question_hop_accuracy[1].append(accuracy)
        elif question_hop == 2:
            question_hop_accuracy[2].append(accuracy)
        elif question_hop == 3:
            question_hop_accuracy[3].append(accuracy)
        else:
            question_hop_accuracy['greater_than_3'].append(accuracy)
        
        if entity_num == 1:
            entity_num_accuracy[1].append(accuracy)
        elif entity_num == 2:
            entity_num_accuracy[2].append(accuracy)
        elif entity_num == 3:
            entity_num_accuracy[3].append(accuracy)
        elif entity_num > 3:
            entity_num_accuracy['greater_than_3'].append(accuracy)

    average_accuracy = total_accuracy / total_samples
    def calculate_group_average(accuracy_dict):
        for k, v in accuracy_dict.items():
            print(len(v))
        return {k: (sum(v) / len(v) if len(v) > 0 else 0) for k, v in accuracy_dict.items()}
    
    question_hop_avg = calculate_group_average(question_hop_accuracy)
    entity_num_avg = calculate_group_average(entity_num_accuracy)
    
    return average_accuracy, question_hop_avg, entity_num_avg


predictions_file = ''

average_accuracy, question_hop_avg, entity_num_avg = calculate_accuracy(predictions_file)

print(f"{average_accuracy}")
print(f"{question_hop_avg}")
print(f"{entity_num_avg}")
