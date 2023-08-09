import numpy as np
import pandas as pd
import Human_Rights_Lab as hrl
from country_dicts import name_to_alpha_2
from country_dicts import alpha_2_to_name

ransom_data = pd.read_csv("cleaned_data/year-country_with_sanctions.csv")
ransom_data = hrl.CountryCodes(ransom_data, "Location (State)", name_to_alpha_2)

gci2018 = pd.read_csv("raw_data/gci2018.csv")
gci2018 = hrl.CountryCodes(gci2018, 'Member State', name_to_alpha_2)
gci2020 = pd.read_csv("raw_data/gci2020.csv")
gci2020 = hrl.CountryCodes(gci2020, 'Member State', name_to_alpha_2)

ransom_2018 = hrl.YearCutoff(ransom_data, "Year", 2017, 2019)
ransom_2020 = hrl.YearCutoff(ransom_data, "Year", 2020, 2022)

def ApplyScore(x, scores, data_country_col, score_country_col, score_score_col):
    country = x[data_country_col]
    score = scores.loc[scores[score_country_col] == country, score_score_col]
    return score.values[0]

def CreateScoreCol(data, scores, data_country_col, score_country_col, score_score_col, new_col_name):
    scores = data.apply(lambda x: ApplyScore(x, scores, data_country_col, score_country_col, score_score_col), axis = 1)
    data[new_col_name] = scores
    return data

cats = ["Score", "Legal Measures", "Technical Measures", "Organizational Measures", "Capacity Development", "Cooperative Measures"]
for cat in cats:
    ransom_2018 = CreateScoreCol(ransom_2018, gci2018, "Location (State)", "Member State", cat, new_col_name = cat)
ransom_2018

cats = ["Score", "Legal Measures", "Technical Measures", "Organizational Measures", "Capacity Development", "Cooperative Measures"]
for cat in cats:
    ransom_2020 = CreateScoreCol(ransom_2020, gci2020, "Location (State)", "Member State", cat, new_col_name = cat)
ransom_2020

ransom_data = pd.concat([ransom_2018, ransom_2020], axis = 0, ignore_index=True)
ransom_data = hrl.CountryCodes(ransom_data, "Location (State)", alpha_2_to_name)
ransom_data.to_csv("cleaned_data/year-country_sanctions+gci_metrics.csv")

