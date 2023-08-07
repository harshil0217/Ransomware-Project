import pandas as pd
import numpy as np
from country_dicts import name_to_alpha_2
from country_dicts import alpha_2_to_name

sanctions = pd.read_csv("raw_data/GSDB_V3.csv")
sanctions = sanctions.drop(["case_id","descr_trade", "arms", "military", "other", "target_mult",
                           "sender_mult", "objective", "success"],  axis = 1)
ransom_data = pd.read_csv("cleaned_data/year-country_transformed.csv")

from Human_Rights_Lab import SplitCountries

sanctions = SplitCountries(sanctions, "sanctioning_state",delim = ", ")
sanctions