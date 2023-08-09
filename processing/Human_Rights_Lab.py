


#Functions to split entries which contain a list of multiple countries
def HandleSplit(x, delim, data, col):
    if isinstance(x[col], str):
        x[col] = x[col].split(delim)
    return x
        
def SplitCountries(data, col, delim = ', '):
    data = data.apply(lambda x: HandleSplit(x, delim, data, col), axis = 1)
    data = data.explode(col, ignore_index = True)
    return data

#Functions to convert country names into standardized ISO-2 country codes
def CheckKeys(x, c_dict, not_in_dict):
    if not_in_dict == False:
        if x in c_dict.keys():
            return c_dict[x]
        else:
            return x
    else:
        return c_dict[x]
    
def CountryCodes(data, country_col, c_dict, not_in_dict = True):
    countries = data[country_col]
    countries = countries.apply(lambda x: CheckKeys(x, c_dict, not_in_dict))
    data[country_col] = countries
    return data

#functions to remove rows containing certain locations
def IncludeCountry(x, countries, country_col, filter_out):
    if filter_out == True:
        if x[country_col] in countries:
            return False
        return True
    else:
        if x[country_col] in countries:
            return True
        return False

def RemoveLoc(data, countries, country_col, filter_out = True):
    include = data.apply(lambda x: IncludeCountry(x, countries, country_col, filter_out), axis = 1)
    data = data[include]
    return data

#functions to filter the data to only include certain years
def Between(x, year_col, begin, end):
    if int(x[year_col]) >= begin and int(x[year_col]) <= end:
        return True
    else:
        return False
    
def YearCutoff(data, year_col, begin, end):
    locs = data.apply(lambda x: Between(x, year_col, begin, end), axis = 1)
    data = data[locs]
    data = data.reset_index()
    return data

#Function to convert organizations to their constituent countries then explode the dataframe

def ApplyOrg(x, country_col, org_list):
    if x[country_col] in org_list.keys():
        x[country_col] = org_list[x[country_col]]
    return x

def ConvertOrgs(data, country_col, org_list):
    data = data.apply(lambda x: ApplyOrg(x, country_col, org_list), axis = 1)
    data = data.explode(country_col, ignore_index = True)
    return data

#function to create a score column

def ApplyScore(x, scores, data_country_col, score_country_col, score_score_col, 
               year_sensitive, data_year_col, score_year_col):
    country = x[data_country_col]
    if year_sensitive == False:
        score = scores.loc[scores[score_country_col] == country, score_score_col]
        if score.shape[0] == 0:
            return "N/A"
        else:
            return score.values[0]
    else:
        year = x[data_year_col]
        score = scores.loc[(scores[score_country_col] == country) & (scores[score_year_col] == year), 
                           score_score_col]
        if score.shape[0] == 0:
            return "N/A"
        else:
            return score.values[0]

def CreateScoreCol(data, scores, data_country_col, score_country_col, score_score_col, new_col_name, 
                   year_sensitive = False, data_year_col = None, score_year_col = None):
    scores = data.apply(lambda x: ApplyScore(x, scores, data_country_col, score_country_col,
                                              score_score_col, year_sensitive, data_year_col, 
                                              score_year_col), axis = 1)
    data[new_col_name] = scores
    return data





    

