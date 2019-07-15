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


def fix_results(file_results1, file_results2, fixed_file_name1, fixed_file_name2):
    with open(file_results1, "r") as judge_results1, open(file_results2, "r") as judge_results2:
        with open(fixed_file_name1, "w") as fixed_judge_results1, open(fixed_file_name2, "w") as fixed_judge_results2:
            for line1, line2 in zip(judge_results1.readlines(), judge_results2.readlines()):
                new_name_line, old_name_line, winner1, vote1, concepts_num_new, concepts_num_old = line1.replace(" ", "").split(",")
                _, _, winner2, vote2, _, _ = line2.replace(" ", "").split(",")

                new_name = results[quetsions_header[question_number]][int(new_name_line)]
                old_name = results_old[quetsions_header[question_number]][int(old_name_line)]

                concepts_num_new_fixed = get_answer_concpets_number(new_name, 0, quetsions_header[question_number])
                concepts_num_old_fixed = get_answer_concpets_number(old_name, 1, quetsions_header[question_number])
                if concepts_num_new_fixed == 0 or concepts_num_old_fixed == 0:
                    continue
                new_name_line, old_name_line, winner1, vote1, concepts_num_new_fixed, concepts_num_old_fixed = str(new_name_line), str(old_name_line), str(winner1), str(vote1), str(concepts_num_new_fixed), str(concepts_num_old_fixed)
                
                fixed_line1 = new_name_line + ", " + old_name_line + ", " + winner1 + ", " + vote1 + ", " +  concepts_num_new_fixed + ", " + concepts_num_old_fixed + "\n"
                fixed_line2 = new_name_line + ", " + old_name_line + ", " + winner2 + ", " + vote2 + ", " +  concepts_num_new_fixed + ", " + concepts_num_old_fixed + "\n"
                
                fixed_judge_results1.write(fixed_line1)
                fixed_judge_results2.write(fixed_line2)


results_old = pd.read_csv("..\\results\\results_old.csv")
results = pd.read_csv("..\\results\\results.csv")
quetsions_header = open("quetions for judges.txt", "r").read().split("\n")

judge_name1 = "Dana"
judge_name2 = "Shimon"

for question_number in range(0, 22):
    file_name1 = "judges_results_original\\" + judge_name1 + "_results_" + quetsions_header[question_number] + ".txt"
    file_name2 = "judges_results_original\\" + judge_name2 + "_results_" + quetsions_header[question_number] + ".txt"

    fixed_file_name1 = "judges_results\\" + judge_name1 + "_results_" + quetsions_header[question_number] + ".txt"
    fixed_file_name2 = "judges_results\\" + judge_name2 + "_results_" + quetsions_header[question_number] + ".txt"

    fix_results(file_name1, file_name2, fixed_file_name1, fixed_file_name2)
        

