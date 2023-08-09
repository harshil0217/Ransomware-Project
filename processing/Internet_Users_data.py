import numpy as np
import pandas as pd
import Human_Rights_Lab as hrl
from country_dicts import name_to_alpha_2
from country_dicts import alpha_3_to_alpha_2
from country_dicts import alpha_2_to_name

user_data = pd.read_csv("raw_data/internet_users_data.csv", skiprows = 3)
user_data = user_data.drop(["Indicator Name", "Indicator Code"], axis = 1)
user_data = user_data.fillna(method = "ffill", axis = 1)
user_data = user_data.drop(columns = user_data.columns[2:59])
user_data = user_data.drop(columns = ["Country Name"])

user_data = hrl.CountryCodes(user_data, "Country Code", alpha_3_to_alpha_2, not_in_dict = False)
user_data = hrl.RemoveLoc(user_data, alpha_2_to_name.keys(), "Country Code", filter_out= False)

user_data = user_data.melt(id_vars= ["Country Code"], 
                           value_vars = ["2017", "2018", "2019", "2020","2021", "2022"], 
                           var_name = "Year", value_name = "Users", ignore_index= True)

user_data["Year"] = user_data["Year"].astype(int)

ransom_data = pd.read_csv("cleaned_data/sanctions+gci_metrics+breach_data.csv")
ransom_data = hrl.CountryCodes(ransom_data, "Location (State)", name_to_alpha_2)

ransom_data = hrl.CreateScoreCol(ransom_data, user_data, "Location (State)", "Country Code", "Users", 
                                 "Internet Users", True, "Year", "Year")

ransom_data = hrl.CountryCodes(ransom_data, "Location (State)", alpha_2_to_name)
ransom_data.to_csv("final_output/ransomware_data_processed.csv", index = False)
