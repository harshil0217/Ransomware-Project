import pandas as pd
import numpy as np
import Human_Rights_Lab as hrl
from country_dicts import name_to_alpha_2
from country_dicts import alpha_2_to_name

ransom_data = pd.read_csv("cleaned_data/year-country_sanctions+gci_metrics.csv")
ransom_data = hrl.CountryCodes(ransom_data, "Location (State)", name_to_alpha_2)

breach_data = pd.read_csv("raw_data/data_breach_statistics.csv", keep_default_na=False)
ransom_data = hrl.CreateScoreCol(ransom_data, breach_data, "Location (State)", "Iso-2", "Average", 
                                 new_col_name = "Breach Incidents")

ransom_data = hrl.CountryCodes(ransom_data, "Location (State)", alpha_2_to_name)
ransom_data.to_csv("cleaned_data/sanctions+gci_metrics+breach_data.csv", index = False)