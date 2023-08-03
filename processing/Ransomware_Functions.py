


#Functions to split entries which contain a list of multiple countries
def HandleSplit(x, delim, data):
    if isinstance(x["Location (State)"], str):
        x["Location (State)"] = x["Location (State)"].split(delim)
    return x
        
def SplitCountries(data, delim = ', '):
    data = data.apply(lambda x: HandleSplit(x, delim, data), axis = 1)
    data = data.explode("Location (State)", ignore_index = True)
    return data

#Functions to convert country names into standardized ISO-2 country codes
def CheckKeys(x, c_dict):
    if x in c_dict.keys():
        return c_dict[x]
    else:
        return x
    
def CountryCodes(data, country_col, c_dict):
    countries = data[country_col]
    countries = countries.map(lambda x: CheckKeys(x, c_dict))
    data[country_col] = countries
    return data

#functions to remove rows containing certain locations
def IncludeCountry(x, to_remove, country_col, filter_out):
    if filter_out == True:
        if x[country_col] in to_remove:
            return False
        return True
    else:
        if x[country_col] in to_remove:
            return True
        return False

def RemoveLoc(data, to_remove, country_col, filter_out = True):
    include = data.apply(lambda x: IncludeCountry(x, to_remove, country_col, filter_out), axis = 1)
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

#Function to add rows of zero for the countries not included without ransom incidents



    

