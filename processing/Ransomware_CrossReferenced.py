import pandas as pd
import numpy as np
from country_dicts import name_to_alpha_2
from country_dicts import alpha_2_to_name
from Human_Rights_Lab import CountryCodes

sanctions = pd.read_csv("raw_data/GSDB_V3.csv")
sanctions = sanctions.drop(["case_id","descr_trade", "arms", "military", "other", "target_mult",
                           "sender_mult", "objective", "success"],  axis = 1)
sanctions = CountryCodes(sanctions, "sanctioned_state", name_to_alpha_2, not_in_dict=False)
sanctions = CountryCodes(sanctions, "sanctioning_state", name_to_alpha_2, not_in_dict=False)

ransom_data = pd.read_csv("cleaned_data/year-country_transformed.csv")
ransom_data = CountryCodes(ransom_data, "Location (State)",name_to_alpha_2)


from Human_Rights_Lab import SplitCountries
from Human_Rights_Lab import ConvertOrgs
from country_dicts import country_orgs

for key in country_orgs:
    country_list = country_orgs[key]
    for i in range(len(country_list)):
        country_list[i] = name_to_alpha_2[country_list[i]]
    country_orgs[key] = country_list

sanctions = SplitCountries(sanctions, "sanctioning_state",delim = ", ")
sanctions = ConvertOrgs(sanctions, "sanctioning_state", country_orgs)
sanctions = CountryCodes(sanctions, "sanctioning_state", name_to_alpha_2, not_in_dict=False)

from Human_Rights_Lab import RemoveLoc

sanctions = RemoveLoc(sanctions, ["UN", "Kimberly Process Participants", "Commonwealth", "North"], "sanctioning_state")

def find_matches(x, country, year, target_country, col):
    if (target_country == "all" and col == "N/A"):
        if (x["sanctioning_state"] == country and x["begin"] <= year and x["end"] >= year):
            return True
    elif(target_country != "all" and col == "sanctioned_state"):
        if (x["sanctioning_state"] == country and x["begin"] <= year and x["end"] >= year and x["sanctioned_state"] == target_country):
            return True
    elif(target_country == "all" and col != "sanctioned_state"):
        if (x["sanctioning_state"] == country and x["begin"] <= year and x["end"] >= year and x[col] == 1):
            return True
    return False

sanctions = sanctions.fillna(0)

def return_counts(data, country, year, target_country, col):
    #matches = data.apply(lambda x: find_matches(x, country, year, target_country, col), axis = 1)
    #length = np.count_nonzero(matches)
    #return (length)
    condition1 = data["sanctioning_state"] == country
    condition2 = data["begin"] <= year
    condition3 = data["end"] >= year
    if (target_country == "all" and col == "N/A"):
        filtered = sanctions.where((condition1 & condition2 & condition3), 0)
        length = np.count_nonzero(filtered["sanctioning_state"])
        return length
    elif(target_country != "all" and col == "sanctioned_state"):
        condition4 = data["sanctioned_state"] == target_country
        filtered = sanctions.where((condition1 & condition2 & condition3 & condition4), 0)
        length = np.count_nonzero(filtered["sanctioning_state"])
        return length
    elif(target_country == "all" and col != "sanctioned_state"):
        condition5 = data[col] == 1
        filtered = sanctions.where((condition1 & condition2 & condition3 & condition5), 0)
        length = np.count_nonzero(filtered["sanctioning_state"])
        return length

def active_sanctions(ransom_data, sanctions_data, new_col_name, target_country = "all", col = "N/A"):
    counts = ransom_data.apply(lambda x: return_counts(sanctions_data, x["Location (State)"], x["Year"], target_country, col), axis = 1)
    ransom_data[new_col_name] = counts
    return ransom_data

ransom_data = active_sanctions(ransom_data, sanctions, "Active Sanctions")

ransom_data = active_sanctions(ransom_data, sanctions, "Iran Sanctions", target_country = "IR", col = "sanctioned_state")
ransom_data = active_sanctions(ransom_data, sanctions, "China Sanctions", target_country = "CN", col = "sanctioned_state")
ransom_data = active_sanctions(ransom_data, sanctions, "Russia Sanctions", target_country = "RU", col = "sanctioned_state")
ransom_data = active_sanctions(ransom_data, sanctions, "North Korea Sanctions", target_country = "KP", col = "sanctioned_state")
ransom_data = active_sanctions(ransom_data, sanctions, "Trade Sanctions", col = "trade")
ransom_data = active_sanctions(ransom_data, sanctions, "Financial Sanctions", col = "financial")
ransom_data = active_sanctions(ransom_data, sanctions, "Travel Sanctions", col = "travel")


ransom_data.to_csv("cleaned_data/year-country_with_sanctions.csv", index = False)