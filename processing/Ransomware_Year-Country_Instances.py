import pandas as pd
import numpy as np
import sys
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

#restricting country list to those only within the gci country database
gci2018 = pd.read_csv("raw_data/gci2018.csv")
gci2018 = CountryCodes(gci2018, "Member State", name_to_alpha_2)
gcicountries = gci2018["Member State"]
ransom_data = RemoveLoc(ransom_data, list(gcicountries), "Location (State)", filter_out= False)
ransom_data

#Converting contents of infrastructure columns to be all uppercase to avoid case issues
ransom_data["Primary CI Sector targeted"] = ransom_data["Primary CI Sector targeted"].str.upper()
ransom_data["Secondary CI Sector"] = ransom_data["Secondary CI Sector"].str.upper()
ransom_data["PaidStatus"] = ransom_data["PaidStatus"].str.upper()

#transform dataframe into year-country instances with counts for each categorical variable
cols_to_encode = ransom_data.columns[3:]
ransom_data = pd.get_dummies(ransom_data, prefix = '', prefix_sep= '',columns = cols_to_encode)
ransom_data = ransom_data.groupby(ransom_data.columns, axis = 1, sort = False).sum()
ransom_data = ransom_data.groupby(['Year', 'Location (State)'], sort = False, as_index = False).sum()
ransom_data = ransom_data.drop("index", axis = 1)

#Convert country names back to standard form
ransom_data = CountryCodes(ransom_data, "Location (State)", alpha_2_to_name)

#Output dataframe to cleaned_data folder
ransom_data.to_csv("cleaned_data/year-country_transformed.csv")




