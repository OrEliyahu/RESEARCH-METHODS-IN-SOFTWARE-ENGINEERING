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


def show_answers_from_file(file_results1, file_results2):
    with open(file_results1, "r") as judge_results1, open(file_results2, "r") as judge_results2:
        winner_counter_old, winner_counter_new = 0, 0
        vote_counter1, vote_counter2 = 0, 0
        concepts_new_avg, concepts_old_avg, winner_concepts_avg, judges_agree = 0, 0, 0, 0
        less_concepts_choosed, more_concepts_choosed = 0, 0
        longer_choosed, shorter_choosed = 0, 0
        number_of_lines = 0        

        for line1, line2 in zip(judge_results1.readlines(), judge_results2.readlines()):
            number_of_lines += 1
            new_name_line, old_name_line, winner1, vote1, concepts_num_new, concepts_num_old = line1.replace(" ", "").split(",")
            _, _, winner2, vote2, _, _ = line2.replace(" ", "").split(",")

            new_name = results[quetsions_header[question_number]][int(new_name_line)]
            old_name = results_old[quetsions_header[question_number]][int(old_name_line)]

            concepts_num_new_fixed = get_answer_concpets_number(new_name, 0, quetsions_header[question_number])
            concepts_num_old_fixed = get_answer_concpets_number(old_name, 1, quetsions_header[question_number])


            if winner1 == winner2:
                judges_agree += 1
                if winner1 == "1":
                    winner_counter_new += 1                
                    winner_concepts_avg += concepts_num_new_fixed
                    
                    if concepts_num_new_fixed > concepts_num_old_fixed:
                        more_concepts_choosed += 1
                    elif concepts_num_new_fixed < concepts_num_old_fixed:
                        less_concepts_choosed += 1

                    if len(new_name) > len(old_name):
                        longer_choosed += 1
                    elif len(new_name) < len(old_name):
                        shorter_choosed += 1

                else:
                    winner_counter_old += 1                  
                    winner_concepts_avg += concepts_num_old_fixed
                                        
                    if concepts_num_new_fixed < concepts_num_old_fixed:
                        more_concepts_choosed += 1
                    elif concepts_num_new_fixed > concepts_num_old_fixed:
                        less_concepts_choosed += 1

                    if len(new_name) < len(old_name):
                        longer_choosed += 1
                    elif len(new_name) > len(old_name):
                        shorter_choosed += 1

            if vote1 == "1":
                vote_counter1 += 1
            else:
                vote_counter2 += 1

            if vote2 == "1":
                vote_counter1 += 1
            else:
                vote_counter2 += 1
                        
            concepts_new_avg += concepts_num_new_fixed            
            concepts_old_avg += concepts_num_old_fixed


        concepts_new_avg /= number_of_lines
        concepts_old_avg /= number_of_lines
        winner_concepts_avg /= judges_agree

        return {"model_wins" : winner_counter_new,
                   "no_model_wins" : winner_counter_old,
                   "time_judges_agree" : judges_agree,
                   "votes_for_first" : vote_counter1,
                   "votes_for_second" : vote_counter2,
                   "model_concepts_avg" : concepts_new_avg,
                   "no_model_concepts_avg" : concepts_old_avg,
                   "winner_concepts_avg" : winner_concepts_avg,
                   "times_more_concepts_win" : more_concepts_choosed,
                   "times_less_concepts_win" : less_concepts_choosed,
                   "times_longer_win" : longer_choosed,
                   "times_shorter_win" : shorter_choosed,
                   "comparisions_number" : number_of_lines,
            }                            
            

if not os.path.exists("judges_results"):
    os.makedirs("judges_results")

results_old = pd.read_csv("..\\results\\results_old.csv")
results = pd.read_csv("..\\results\\results.csv")
quetsions_header = open("quetions for judges.txt", "r").read().split("\n")

judge_name1 = "Dana"
judge_name2 = "Shimon"

for question_number in range(0, 22):
    file_name1 = "judges_results\\" + judge_name1 + "_results_" + quetsions_header[question_number] + ".txt"
    file_name2 = "judges_results\\" + judge_name2 + "_results_" + quetsions_header[question_number] + ".txt"

    with open("results_summery\\" + quetsions_header[question_number] + ".json", "w") as results_file:
        json.dump(show_answers_from_file(file_name1, file_name2), results_file, indent=4)


model_win = 0
no_model_win = 0
more_concepts_win = 0
less_concepts_win = 0
longer_win = 0
shorter_win = 0
votes_for_first = 0
votes_for_second = 0
comparisions_number = 0

for file_summey in os.listdir("results_summery"):
    json_file = open("results_summery\\" + file_summey)
    summery = json.loads(json_file.read())    
    model_win += summery["model_wins"]
    no_model_win += summery["no_model_wins"]
    more_concepts_win += summery["times_more_concepts_win"]
    less_concepts_win += summery["times_less_concepts_win"]
    longer_win += summery["times_longer_win"]
    shorter_win += summery["times_shorter_win"]
    votes_for_first += summery["votes_for_first"]
    votes_for_second += summery["votes_for_second"]
    comparisions_number += summery["comparisions_number"]


with open("summery_results.json", "w") as results_file:
    final_results = {"total_model_wins" : model_win,
                     "total_no_model_wins" : no_model_win,
                     "total_more_concepts_wins" : more_concepts_win,
                     "total_less_concepts_wins" : less_concepts_win,
                     "total_votes_for_first" : votes_for_first,
                     "total_votes_for_second" : votes_for_second,
                     "total_votes_for_longer" : longer_win,
                     "total_votes_for_shorter" : shorter_win,
                     "total_comparisions" : comparisions_number,
        }

    json.dump(final_results, results_file, indent=4)
