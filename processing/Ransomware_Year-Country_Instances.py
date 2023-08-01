import pandas as pd
import numpy as np
import sys
from sklearn.preprocessing import OneHotEncoder
from country_dicts import name_to_alpha_2
from country_dicts import alpha_2_to_name
from country_dicts import us_states

ransom_data = pd.read_csv("raw_data/RansomwareRepository_v12.4.csv")

ransom_data = ransom_data.drop(['ID Number', 'Date_Began', 
                                'General_Date (if date_began unknown)','OrgName', 'State', 
                                'County', 'County', 'Strain', 
                                'Duration (days, unless specified)',
                                'Ransom Amount', 'Local Currency', 
                                "MITRE ATT&CK Software ID [if exists]",
                                "PayMethod (only if paid)", "AmtPaid", "Source", 
                                "Related incidents", "Comments"], axis = 1)

from Ransomware_Functions import SplitCountries

ransom_data = SplitCountries(ransom_data)
ransom_data = SplitCountries(ransom_data, " and ")
ransom_data = SplitCountries(ransom_data, "and ")

for state in us_states:
    ransom_data = ransom_data.replace(state, us_states[state])

ransom_data = ransom_data.dropna(subset = ["Year", "Location (State)"])
ransom_data = ransom_data.reset_index(drop = True)

from Ransomware_Functions import YearCutoff
ransom_data = YearCutoff(ransom_data, "Year", 2017, 2022)

from Ransomware_Functions import RemoveLoc
ransom_data = RemoveLoc(ransom_data, ["Global", "Undisclosed", "PEI", "Europe", "GCC Region",
                                       "Middle East", "North Africa", "Arab Region", 
                                       "Unspecified", "Global ", "Asia", "Scandinavia", 
                                       "North America", "Africa"], "Location (State)")

from country_dicts import CountryCodes
ransom_data = CountryCodes(ransom_data, "Location (State)", name_to_alpha_2)
ransom_data

#restricting country list to those only within the gci country database


