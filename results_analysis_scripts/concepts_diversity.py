import ast
import random
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
from os import listdir


RANDOM_FACTOR = 5


def generate_random_answers(data, answers_number):
    selected = random.sample(range(1, len(data)), answers_number)
    selected_data = [data[0]] + [data[i] for i in selected]
    return selected_data


def cocepts_dist(data):
    concepts_distribution = {}
    for i in range(1, len(data[0])):
        for j in range(1, len(data)):
            if data[j][i]:
                if data[0][i] not in concepts_distribution:
                    concepts_distribution[data[0][i]] = []
                concepts_distribution[data[0][i]] += [data[j][i]]
        if data[0][i] in concepts_distribution:
            concepts_distribution[data[0][i]] = dict(Counter(concepts_distribution[data[0][i]]))
    return concepts_distribution


def add_to_counters(sum_dict, dict_to_add):
    for concept in dict_to_add:
        for word in dict_to_add[concept]:
            if concept not in sum_dict:
                sum_dict[concept] = {}
            if word not in sum_dict[concept]:
                sum_dict[concept][word] = 0
            sum_dict[concept][word] += dict_to_add[concept][word]

    return sum_dict


def normalize_concepts_distribution(concepts_distribution, N):
    for concept in concepts_distribution:
        for word in concepts_distribution[concept]:
            concepts_distribution[concept][word] /= N
    return concepts_distribution


def calc_diversity(file_name_old, file_name_new):
    concepts_file_old = open(file_name_old, encoding="utf-8")
    concepts_file_new = open(file_name_new, encoding="utf-8")
    data_old = ast.literal_eval(concepts_file_old.read())
    data_new = ast.literal_eval(concepts_file_new.read())

    data_old_len = len(data_old)
    data_new_len = len(data_new)

    if data_old_len == data_new_len:
        concepts_distribution_old = cocepts_dist(data_old)
        concepts_distribution_new = cocepts_dist(data_new)        
        return concepts_distribution_old, concepts_distribution_new
    
    if data_old_len > data_new_len:
        
        sampled_data = generate_random_answers(data_old, len(data_new) - 1)
        concepts_distribution = cocepts_dist(data_old)
        for i in range(RANDOM_FACTOR - 1):
            sampled_data = generate_random_answers(data_old, len(data_new) - 1)
            concepts_distribution_to_add = cocepts_dist(sampled_data)
            concepts_distribution = add_to_counters(concepts_distribution, concepts_distribution_to_add)
        concepts_distribution = normalize_concepts_distribution(concepts_distribution, RANDOM_FACTOR)
        concepts_distribution_old = concepts_distribution
        concepts_distribution_new = cocepts_dist(data_new)
        return concepts_distribution_old, concepts_distribution_new
        
    else:
        sampled_data = generate_random_answers(data_new, len(data_old) - 1)
        concepts_distribution = cocepts_dist(data_new)
        for i in range(RANDOM_FACTOR):
            sampled_data = generate_random_answers(data_new, len(data_old) - 1)
            concepts_distribution_to_add = cocepts_dist(sampled_data)
            concepts_distribution = add_to_counters(concepts_distribution, concepts_distribution_to_add)
        concepts_distribution = normalize_concepts_distribution(concepts_distribution, RANDOM_FACTOR)
        
        concepts_distribution_old = cocepts_dist(data_old)
        concepts_distribution_new = concepts_distribution
        return concepts_distribution_old, concepts_distribution_new
    

for question_file in listdir("..\\summaries"):
    print(question_file)
    qustion = question_file.split(".")[0]
    old_file = "..\\tables\\" + qustion + "_1.txt"
    new_file = "..\\tables\\" + qustion + "_0.txt"

    concepts_distribution_old, concepts_distribution_new = calc_diversity(old_file, new_file)

    concepts_distribution_old = pd.DataFrame(concepts_distribution_old).T.fillna(0)
    concepts_distribution_new = pd.DataFrame(concepts_distribution_new).T.fillna(0)
    concepts_distribution_old.to_csv('distribution\\old\\old_' + qustion + '.csv', index=True, header=True)
    concepts_distribution_new.to_csv('distribution\\new\\new_' + qustion + '.csv', index=True, header=True)

