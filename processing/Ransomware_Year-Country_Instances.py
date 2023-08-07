import pandas as pd
import numpy as np
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

from Human_Rights_Lab import SplitCountries

ransom_data = SplitCountries(ransom_data, "Location (State)")
ransom_data = SplitCountries(ransom_data, "Location (State)", " and ")
ransom_data = SplitCountries(ransom_data, "Location (State)", "and ")

for state in us_states:
    ransom_data = ransom_data.replace(state, us_states[state])

ransom_data = ransom_data.dropna(subset = ["Year", "Location (State)"])
ransom_data = ransom_data.reset_index(drop = True)

from Human_Rights_Lab import YearCutoff
ransom_data = YearCutoff(ransom_data, "Year", 2017, 2022)

from Human_Rights_Lab import RemoveLoc
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

#insert empty rows for countries withiin the gci database without incidents such that all countries are documented
years = np.unique(ransom_data["Year"])

years_gci = []
for year in years:
    for country in gcicountries:
        years_gci.append([year, country])

years_gci
years_gci = pd.DataFrame(years_gci, columns = ["Year", "GCICountries"])
years_gci

num_zeros = len(ransom_data.columns) - 2

def NewRow(x, ransom_data):
    year = x["Year"]
    country = x["GCICountries"]
    filtered_table = ransom_data.loc[ransom_data["Year"] == year]
    filtered_table = filtered_table.loc[filtered_table["Location (State)"] == country]
    if len(filtered_table) == 0:
        new_row = [x["Year"], x["GCICountries"]] + list(np.zeros(num_zeros))
        new_row_df = pd.Series(new_row, index = ransom_data.columns)
        return new_row_df
    else:
        new_row =  ["REMOVE", "REMOVE"] + list(np.zeros(num_zeros))
        new_row_df = pd.Series(new_row, index = ransom_data.columns)
        return new_row_df
    
new_rows = years_gci.apply(lambda x: NewRow(x, ransom_data), axis = 1, result_type = "expand")
ransom_data = pd.concat([ransom_data, new_rows], axis = 0)
ransom_data

ransom_data = RemoveLoc(ransom_data, "REMOVE", "Location (State)")

#Convert country names back to standard form
ransom_data = CountryCodes(ransom_data, "Location (State)", alpha_2_to_name)
ransom_data = ransom_data.sort_values(by = ["Year", "Location (State)"])

#Output dataframe to cleaned_data folder
ransom_data.to_csv("cleaned_data/year-country_transformed.csv")




