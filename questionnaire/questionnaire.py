import os
from random import randint
import pandas as pd
import ast
import re
import pickle
import json


def fix_answer(answer):
    return re.sub( '(?<!^)(?=[A-Z][a-z])', '_', answer).lower().replace("__", "_")


def ans_to_str(ans):
    return str(ans[0])


def get_answer_concpets_number(answer, old, question):
    file_name = "..\\tables\\" + question + "_" + str(old) + ".txt"

    if not os.path.isfile(file_name):
        return -2

    counter = 0
    answer = fix_answer(answer)
    with open(file_name, "r", encoding="utf-8") as concepts_file:
        concepts = ast.literal_eval(concepts_file.read())
        for i in range(1, len(concepts)):
            if concepts[i][0] == answer:                
                for concept in concepts[i][1:]:
                    if concept:
                        counter += 1
                return counter
    
    return -1


def start_questionnaire(old_names, new_names, answer_header, judge_name):
    same_answer_counter = 0
    with open("judges_results\\" + judge_name + "_results_" + answer_header, "a") as results:
        ROUNDS_NUMBER = 60
        if not os.path.isfile("pickles\\" + answer_header + ".pkl"):
            permotations = []
            for i in range(ROUNDS_NUMBER):
                model_answer = new_names[randint(0, len(new_names) - 1)]
                original_answer = old_names[randint(0, len(old_names) - 1)]
                while not all(ord(char) < 128 for char in original_answer[1]) or not all(ord(char) < 128 for char in model_answer[1]) or fix_answer(model_answer[1]) == fix_answer(original_answer[1]):
                    if fix_answer(model_answer[1]) == fix_answer(original_answer[1]):
                        same_answer_counter += 1
                    model_answer = new_names[randint(0, len(new_names) - 1)]
                    original_answer = old_names[randint(0, len(old_names) - 1)]
            
                permotations += [[original_answer, model_answer]]

            with open("pickles\\" + answer_header + ".pkl", "wb") as f:
                pickle.dump(permotations, f)
        else:            
            with open("pickles\\" + answer_header + ".pkl", "rb") as f:
                permotations = pickle.load(f)
                
        for i in range(ROUNDS_NUMBER):
            original_answer = permotations[i][0]
            model_answer = permotations[i][1]
            order = randint(0, 1)
            old_concept_number = str(get_answer_concpets_number(original_answer[1], 1, answer_header))
            new_concept_number = str(get_answer_concpets_number(model_answer[1], 0, answer_header))
            if order == 0:

                user_answer = input("1. " + model_answer[1] + "\n2. " + original_answer[1] + "\n")
                while(user_answer != "1" and user_answer != "2"):
                    user_answer = input("1. " + model_answer[1] + "\n2. " + original_answer[1] + "\n")

                user_answer = int(user_answer)
                
                if user_answer == 1:
                    results.write(ans_to_str(model_answer) + ", " + ans_to_str(original_answer) + ", " + 
                                  "1" + ", 1, " + new_concept_number + ", " + old_concept_number + "\n")
                else:
                    results.write(ans_to_str(model_answer) + ", " + ans_to_str(original_answer) + ", " + 
                                  "2" + ", 2, " + new_concept_number + ", " + old_concept_number + "\n")

            else:
                
                user_answer = input("1. " + original_answer[1] + "\n2. " + model_answer[1] + "\n")

                while(user_answer != "1" and user_answer != "2"):
                    user_answer = input("1. " + original_answer[1] + "\n2. " + model_answer[1] + "\n")
                
                user_answer = int(user_answer)

                if user_answer == 1:
                    results.write(ans_to_str(model_answer) + ", " + ans_to_str(original_answer) + ", " + 
                                  "2" + ", 1, " + new_concept_number + ", " + old_concept_number + "\n")
                else:
                    results.write(ans_to_str(model_answer) + ", " + ans_to_str(original_answer) + ", " + 
                                  "1" + ", 2, " + new_concept_number + ", " + old_concept_number + "\n")
            print("-------------------------")        


def show_answers_from_file(file_results1, file_results2):
    with open(file_results1, "r") as judge_results1, open(file_results2, "r") as judge_results2:
        winner_counter_old, winner_counter_new = 0, 0
        vote_counter1, vote_counter2 = 0, 0
        concepts_new_avg, concepts_old_avg = 0, 0

        for line1, line2 in zip(judge_results1.readlines(), judge_results2.readlines()):
            new_name_line, old_name_line, winner1, vote1, concepts_num_new, concepts_num_old = line1.replace(" ", "").split(",")
            _, _, winner2, vote2, _, _ = line2.replace(" ", "").split(",")

            if winner1 == winner2:
                if winner1 == "1":
                    winner_counter_new += 1
                else:
                    winner_counter_old += 2
            if vote1 == "1":
                vote_counter1 += 1
            else:
                vote_counter2 += 1

            if vote2 == "1":
                vote_counter1 += 1
            else:
                vote_counter2 += 1

            new_name = results[quetsions_header[question_number]][int(new_name_line)]
            old_name = results_old[quetsions_header[question_number]][int(old_name_line)]

            concepts_num_new_fixed = get_answer_concpets_number(new_name, 0, quetsions_header[question_number])
            concepts_num_old_fixed = get_answer_concpets_number(old_name, 1, quetsions_header[question_number])

            if concepts_num_new_fixed > 0:
                concepts_new_avg += concepts_num_new_fixed
            if concepts_num_old_fixed > 0:
                concepts_old_avg += concepts_num_old_fixed


        concepts_new_avg /= 60
        concepts_old_avg /= 60

        return {"model_wins" : winner_counter_new,
                   "no_model_wins" : winner_counter_old,
                   "votes_for_first" : vote_counter1,
                   "votes_for_second" : vote_counter2,
                   "model_concepts_avg" : concepts_new_avg,
                   "no_model_concepts_avg" : concepts_old_avg,
            }                            
            

if not os.path.exists("judges_results"):
    os.makedirs("judges_results")

results_old = pd.read_csv("..\\results\\results_old.csv")
results = pd.read_csv("..\\results\\results.csv")
quetsions_header = open("quetions for judges.txt", "r").read().split("\n")

judge_name = input("enter your name: ")


for question_number in range(0, 22):
    old_names = [(ind, ans) for ind, ans in enumerate(results_old[quetsions_header[question_number]]) if str(ans) != "nan"][2:-1]
    new_names = [(ind, ans) for ind, ans in enumerate(results[quetsions_header[question_number]]) if str(ans) != "nan"][2:-1]
    start_questionnaire(old_names, new_names, quetsions_header[question_number], judge_name)
