import os
from random import randint
import pandas as pd
import ast
import re
import pickle


def fix_answer(answer):
    return re.sub( '(?<!^)(?=[A-Z][a-z])', '_', answer).lower().replace("__", "_")


def ans_to_str(ans):
    return str(ans[0])


def get_answer_concpets_number(answer, old, question):
    file_name = "..//tables//" + question + "_" + str(old) + ".txt"

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
    with open("judges_results//" + judge_name + "_results_" + answer_header, "a") as results:
        ROUNDS_NUMBER = 60
        if not os.path.isfile("pickles//" + answer_header + ".pkl"):
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

            with open("pickles//" + answer_header + ".pkl", "wb") as f:
                pickle.dump(permotations, f)
        else:            
            with open("pickles//" + answer_header + ".pkl", "rb") as f:
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


def show_answers_from_file(results_file):
    with open(results_file, "r") as judge_results:
        for line in judge_results.readlines():
            if "number of time answers were equals is: " in line:
                continue
            new_name_line, old_name_line, winner, vote, old_concepts_number, new_concepts_number  = line.split(",")
            
            print(results_old[quetsions_header[question_number]][int(old_name_line)])
            print(results[quetsions_header[question_number]][int(new_name_line)])
            if int(winner) == 1:
                print(results[quetsions_header[question_number]][int(new_name_line)])
                print("new")
            elif int(winner) == 2:
                print(results_old[quetsions_header[question_number]][int(old_name_line)])
                print("old")                                        
            

if not os.path.exists("judges_results"):
    os.makedirs("judges_results")

results_old = pd.read_csv("..//results//results_old.csv")
results = pd.read_csv("..//results//results.csv")
quetsions_header = open("quetions for judges.txt", "r").read().split("\n")

judge_name = input("enter your name: ")

question_number = 0 # 0 - 22

old_names = [(ind, ans) for ind, ans in enumerate(results_old[quetsions_header[question_number]]) if str(ans) != "nan"][2:-1]
new_names = [(ind, ans) for ind, ans in enumerate(results[quetsions_header[question_number]]) if str(ans) != "nan"][2:-1]

    
start_questionnaire(old_names, new_names, quetsions_header[question_number], judge_name)    
# show_answers_from_file("judges_results//" + judge_name + "_results_" + quetsions_header[question_number])
