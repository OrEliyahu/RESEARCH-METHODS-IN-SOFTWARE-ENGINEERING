import json
import numpy as np
from os import listdir
import matplotlib.pyplot as plt


def plot_bars(old_data, new_data, ylabel, title, fig_name):
    index = np.arange(len(old_data))
    bar_width = 0.35
    fig, ax = plt.subplots()

    mins = [min(i, j) for i , j in zip(old_data, new_data)]
    ax.bar(index, old_data, bar_width, label="without model", color="blue")
    ax.bar(index, new_data, bar_width, label="with model", color="red")
    ax.bar(index, mins, bar_width, color="purple")

    ax.set_xlabel('qustions')
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_xticks(index)
    ax.set_xticklabels(questions, rotation='vertical')
    ax.legend()

    plt.savefig(fig_name + "_transpeant", transparent=True)


def get_mean_var(file_name):
    with open("..\\summaries\\" + file_name) as json_file:
        data = json.load(json_file)
        return data["variables_lengths_mean_old"], data["variables_lengths_mean_new"], data["variables_lengths_var_old"], data["variables_lengths_var_new"]


means_old = []
means_new = []
vars_old = []
vars_new = []
questions = []


for file_name in listdir("..\\summaries"):
    questions += [file_name.split(".")[0]]
    mean_old, mean_new, var_old, var_new = get_mean_var(file_name)
    means_old += [mean_old]
    means_new += [mean_new]
    vars_old += [var_old]
    vars_new += [var_new]


plot_bars(means_old, means_new, 'variable length mean', "compare variable length mean", "means_length")
plot_bars(vars_old, vars_new, 'variable length variance', "compare variable length variance' variance", "vars_length")