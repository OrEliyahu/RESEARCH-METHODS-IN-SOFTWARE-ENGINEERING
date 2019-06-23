import json
import numpy as np
from os import listdir
import matplotlib.pyplot as plt


def plot_bars(old_data, new_data, ylabel, title, fig_name):
    index = np.arange(len(old_data))
    bar_width = 0.35
    fig, ax = plt.subplots()
    ax.bar(index, old_data, bar_width, label="without model", alpha=0.7, color='blue')
    ax.bar(index, new_data, bar_width, label="with model", alpha=0.7, color='red')

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
        return data["concpets_mean_old"], data["concpets_mean_new"], data["concpets_var_old"], data["concpets_var_new"]


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


plot_bars(means_old, means_new, 'number of concpets mean', "compare number of concepts' mean", "means")
plot_bars(vars_old, vars_new, 'number of concpets variances', "compare number of concepts' variance", "vars")