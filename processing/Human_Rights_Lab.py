


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

#Function to convert organizations to their constituent countries then explode the dataframe

def ApplyOrg(x, country_col, org_list):
    if x[country_col] in org_list.keys():
        x[country_col] = org_list[x[country_col]]
    return x

def ConvertOrgs(data, country_col, org_list):
    data = data.apply(lambda x: ApplyOrg(x, country_col, org_list), axis = 1)
    data = data.explode(country_col, ignore_index = True)
    return data





    

