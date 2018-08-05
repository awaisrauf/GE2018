# -*- coding: utf-8 -*-
"""
Created on Sat Jul 21 05:54:26 2018
@author: Awais: awaisrauf.github.io
@descrption:  Function related to cleaning and preprocessing of raw data
    
"""

import pandas as pd
 
#==============================================================================
# Proprcoesses voter distribution data                 
#==============================================================================
def Vote_distribution_preprocessed():
    df_NA_voter_dist = pd.read_csv("E:\Semester3\GE2018\election\data\Election_2018_Stats\\Voter_Distribution_Lat_Lng.csv")
    #  Change constituency number from format NA-240 Rawalpindi to NA-240
    constituencies = df_NA_voter_dist["Constituency"].str.split(" ")
    constituencies = pd.DataFrame(constituencies.values.tolist()).add_prefix('constituency_')
    constituencies = constituencies.drop(constituencies.columns[[1,2]], axis=1)
    df_NA_voter_dist["Constituency"] = constituencies
    return df_NA_voter_dist                
                   
def NA_list_preprocessed():                    
    df_NA_list = pd.read_csv("E:\Semester3\GE2018\election\data\Election_2018_Stats\\NA_List.csv")
    

    # Replace full party names with their symbols
    # Mannual Replacements are preffered as there are many similar names of parties

    replacements = {
      # standredize Independent name in data      
      'Independent': 'IND',
      'Independent Candidate': 'IND',
      ' Independent': 'IND',
      'Indepdendent': 'IND',
      # standredize PTI name in data
      'Pakistan Tehreek-e-lnsaf':'PTI',
      'Pakistan Tehreek e Insaf': 'PTI',
      'Pakistan Tehreek E Insaf': 'PTI',
      'Pakistan Tehreek e Insaaf': 'PTI',
      'Pakistan tehreek-e-Insaf': 'PTI',
      'Pakistan Tehreek e insaf': 'PTI',
      'PakistanTehreek-e-Insaf':  'PTI',
      'Pakisyan Tehreek e Insaaf': 'PTI',
      'Pakistan Tehreek-e-lnsaf': 'PTI',
      'Pakistan tehreek e Insaf': 'PTI',
      'Pakistan Tehreek-e-Insaf': 'PTI', 
      'Pakistan Tahreek-e-Insafa': 'PTI',
      'Tehrik e Insaf': 'PTI',
      # standredize PML-N name in data
      'Pakistan Muslim League (N)': 'PML-N',
      'Pakistan Muslim League(N)': 'PML-N', 
      'Pakistan Muslim League\n(N)': 'PML-N',                    
      'PMLN': 'PML-N',
      'PMLN': 'PML-N',
      'PML (N)': 'PML-N',
      'PML -N': 'PML-N',   
      'Pakistan Muslim League(N)' : 'PML-N', 
      # standredize PPPP name in data                       
      'Pakistan Peoples Party Parliamentarians': 'PPPP',
      'Pakistan Peoples party parlimentarians':'PPPP',
      'Pakistan Peoples party parlimentarians': 'PPPP',
      'Pakistan Peoples Party Parlimentarians': 'PPPP',
      'Pakistan Peoples Party\nParliamentarians': 'PPPP',
      'Pakistan Peoples Party': 'PPPP',
      'Pakistan Peoples Part Parliamentarians': 'PPPP',
      'Pakistan peopkes party parlimentarians': 'PPPP',
      'Pakistan People Party Parlianmentray': 'PPPP',
      # 
      'MUTAHIDA MAJLIS AMAL PAKISTAN': 'MMA',
      'Mutahida Majlas-e-Amal Pakistan':'MMA',
      'MUTAHIDA MAJLIS AMAL PAKISTAN ': 'MMA',
      'Mutthida Majlis-E-Amal Pakistan': 'MMA',
      'Mutthida Majlis-e-Amal Pakistan': 'MMA',
      'Mutahida Majlas-e-Amal Pakistan': 'MMA',
      'MUTTHIDA MAJLIS-E-AMAL PAKISTAN': 'MMA',
      'MUTTAHIDA MAJLIS-E- AMAL PAKISTAN': 'MMA',
      'Muthida Majlis e Amal Pakistan': 'MMA',
      'Mutihida Majlis e Amal Pakistan': 'MMA',
      'M.M.A' : 'MMA',
      #
      'Mutahida Qaumi Movemebt Pakistan': 'MQM',
      'Muttahida Qaumi Movement Pakistan': 'MQM',
      # 
      'Tehreek Labbaik Pakistan': 'TLP',
      'Tehreek labbaik Pakistan': 'TLP',
      'Tehrik e Labbaik': 'TLP',
      'Tahreek Labbaik pakistan': 'TLP',
      'Tehreek e Labbaik Pakistan': 'TLP',
      'Tehrek e labbaik Pakistan' : 'TLP',
      'Tehrik e Labbaik Pakistan': 'TLP',
      'Tehrik e Labbaik': 'TLP',
      'Tehrik e Labbaik': 'TLP',
      'Tehreek e labbaik Pakistan':'TLP',
      'Tehreek-e-Labbaik Pakistan': 'TLP',
      'Tehreek e Labbaik Pakistan TLI ': 'TLP',
      #
      'Awami National Party': 'ANP',
      'Avvami National Party': 'ANP',
      #
      'Pak Sarzameen Party': 'PSP',
      'Pak SarZamen Party': 'PSP',
      #
      'Pakistan Muslim League': 'PML-Q',
      'PML -Q':'PML-Q',
      #
      'Balochistan National Party': 'BNP',
      'Balochistan National Party': 'BNP',
      #
      'Balochistan Awami Party': 'BAP',
      'Balochistan Awami Party': 'BAP',
      #
      'Pashtoonkhwa Milli Awami Party': 'PKMAP',
      'PashtoonKhwa Milli Awami party': 'PKMAP',
      'Pakhtoonkhwa Milli Awami Party ': 'PKMAP',
      'Pashtoonkhawa Milli Awami Party': 'PKMAP',
      'Pashtunkhwa Milli Awami Party ': 'PKMAP',
      # 
      'All Pakistan Muslim League': 'APML',
      #
      'Grand Democratic Allience': 'GDA',
      'G.D.A': 'GDA',
      #
      'Sindh United Party': 'SUP',
      #
      'Qaumi Watan Party': 'QWP',
      "Pakistan Muslim League (Z)":"PML-Z"
      
    }
    df_NA_list['Party Affiliation'].replace(replacements, inplace=True)
    
    # add a district as a new column by preprocessing constituency name (Rawalpinid-1 to Rawalpinid)
    df_constituency = df_NA_list["Constituency Name"].str.strip()    # remove leading spaces
    cities = (df_constituency.str.split(" "))                        # strips names based on spaces
    cities_1 = pd.DataFrame(cities.values.tolist()).add_prefix('constituency_')  # retain column that only have district name
    cities_1  = cities_1.drop(cities_1.columns[[1, 2, 3, 4, 5]],axis=1)
    cities_1 = cities_1["constituency_0"].str.split("-")
    cities_1 = pd.DataFrame(cities_1.values.tolist()).add_prefix('constituency_')
    cities_1  = cities_1.drop(cities_1.columns[[1, 2, 3, 4 ]],axis = 1)
    df_NA_list["District"] = cities_1["constituency_0"].str.lower()
    
    # solving mismatching districts problem
    replacement_districts = {
            "gwadar": "gawadar",
            "jacababd":"jacobabad",
            "jackoabad":"jacobabad",
            "batagram":"battagram",
            "d.g.":"dgkhan",
            "d.i.khan":"dikhan",
            "gujrnawala":"guranwala",
            "sba":"jaffarabad",
            "bolan":"kachhi",
            "lower.dir":"lower",
            "upper.dir":"upper",
            "r.y.khan":"ryk",
            "rahim":"ryk",
            "sahib":"nankana",
            "shikarpu":"shikarpur",
            "t.t.singh":"toba",
            "mastun":"mastung",
            "sujawal":"thatta",
            "sakkar":"sukkar"
            }
    df_NA_list['District'].replace(replacement_districts, inplace=True)
    
    # Remove space in constituencies names i.e. if cons_name = "NA-1 ", make it "NA-1"
    number_of_constituencies = len(df_NA_list["Constituency Number (ID)"].tolist())
    list_corrected_names = []
    for i in range(number_of_constituencies):
        corrected_name =  df_NA_list["Constituency Number (ID)"].iloc[i].strip()
        list_corrected_names.append(corrected_name)
    # replace all the values    
    df_NA_list.loc[0:number_of_constituencies,"Constituency Number (ID)"] = list_corrected_names
    return df_NA_list

#==============================================================================
# Adds district name from constituency name
# Converts percentage from 55% values to 55 like ints
# Fills nan values in party column with IND = Independent
#==============================================================================
def Perevious_results_preprocessed():
    df_perevious_results = pd.read_csv("E:\Semester3\GE2018\election\data\Perevious_Results\Previous_Elections_1997-2013.csv")

    # add a district as a new column by preprocessing constituency name
    df_constituency = df_perevious_results["constituency"].str.strip()
    cities = (df_constituency.str.split(" "))
    abc = pd.DataFrame(cities.values.tolist()).add_prefix('constituency_')
    abc  = abc.drop(abc.columns[[0, 2, 3, 4, 5, 6]], axis=1)
    abc = abc["constituency_1"].str.split("-")
    abc = pd.DataFrame(abc.values.tolist()).add_prefix('constituency_')
    abc  = abc.drop(abc.columns[[1, 2, 3, 4, 5, 6]], axis=1)
    df_perevious_results["District"] = abc["constituency_0"].str.lower()
    # solving mismatching districts problem
    replacement_districts = {
            "gwadar": "gawadar",
            "jacababd":"jacobabad",
            "jackoabad":"jacobabad",
            "batagram":"battagram",
            "d.g.":"dgkhan",
            "d.i.khan":"dikhan",
            "gujrnawala":"guranwala",
            "sba":"jaffarabad",
            "bolan":"kachhi",
            "lower.dir":"lower",
            "upper.dir":"upper",
            "r.y.khan":"ryk",
            "rahim":"ryk",
            "sahib":"nankana",
            "shikarpu":"shikarpur",
            "t.t.singh":"toba",
            "mastun":"mastung",
            "sujawal":"thatta",
            "sakkar":"sukkar",
            "k":"karachi",
            "korang":"karachi",
            "malir":"karachi"
            }
    df_perevious_results['District'].replace(replacement_districts, inplace=True)     

                   
    # change turnout from percentage(e.g. 55%) to int (e.g. 55)                    
    turnout = df_perevious_results["Turnout"].str.split("%")
    turnout = pd.DataFrame(turnout.values.tolist()).add_prefix('turnout_')
    turnout  = turnout.drop(turnout.columns[[1]], axis=1).astype(float)
    df_perevious_results["Turnout"] = turnout
                        
    # fills nan values in party affiliation with IND
    df_perevious_results["Party"].fillna("IND", inplace = True) 

    # replace PML with PML-Q as its name was changes
    df_perevious_results["Party"].replace("PML","PML-Q", inplace = True)                   
    return df_perevious_results                     
#==============================================================================
# Preprocessed result 2018
# 
#==============================================================================
def Result_2018():
    df_result_2018 = pd.read_csv("E:\Semester3\GE2018\GE2018\election_prediction\data\Election_2018_Stats\Election_result_2018.csv")
    # fill na values with values above
    df_result_2018 = df_result_2018.fillna(method="ffill")
    
    replacements = {
          # standredize Independent name in data      
          'Independent': 'IND',
          'Independent Candidate': 'IND',
          ' Independent': 'IND',
          'Indepdendent': 'IND',
          # standredize PTI name in data
          'Pakistan Tehreek-e-lnsaf':'PTI',
          'Pakistan Tehreek e Insaf': 'PTI',
          'Pakistan Tehreek E Insaf': 'PTI',
          'Pakistan Tehreek e Insaaf': 'PTI',
          'Pakistan tehreek-e-Insaf': 'PTI',
          'Pakistan Tehreek e insaf': 'PTI',
          'PakistanTehreek-e-Insaf':  'PTI',
          'Pakisyan Tehreek e Insaaf': 'PTI',
          'Pakistan Tehreek-e-lnsaf': 'PTI',
          'Pakistan tehreek e Insaf': 'PTI',
          'Pakistan Tehreek-e-Insaf': 'PTI', 
          'Pakistan Tahreek-e-Insafa': 'PTI',
          'Tehrik e Insaf': 'PTI',
          # standredize PML-N name in data
          'Pakistan Muslim League (N)': 'PML-N',
          'Pakistan Muslim League(N)': 'PML-N', 
          'Pakistan Muslim League\n(N)': 'PML-N',                    
          'PMLN': 'PML-N',
          'PMLN': 'PML-N',
          'PML (N)': 'PML-N',
          'PML -N': 'PML-N',   
          'Pakistan Muslim League(N)' : 'PML-N', 
          # standredize PPPP name in data                       
          'Pakistan Peoples Party Parliamentarians': 'PPPP',
          'Pakistan Peoples party parlimentarians':'PPPP',
          'Pakistan Peoples party parlimentarians': 'PPPP',
          'Pakistan Peoples Party Parlimentarians': 'PPPP',
          'Pakistan Peoples Party\nParliamentarians': 'PPPP',
          'Pakistan Peoples Party': 'PPPP',
          'Pakistan Peoples Part Parliamentarians': 'PPPP',
          'Pakistan peopkes party parlimentarians': 'PPPP',
          'Pakistan People Party Parlianmentray': 'PPPP',
          # 
          'MUTAHIDA MAJLIS AMAL PAKISTAN': 'MMA',
          'Mutahida Majlas-e-Amal Pakistan':'MMA',
          'MUTAHIDA MAJLIS AMAL PAKISTAN ': 'MMA',
          'Mutthida Majlis-E-Amal Pakistan': 'MMA',
          'Mutthida Majlis-e-Amal Pakistan': 'MMA',
          'Mutahida Majlas-e-Amal Pakistan': 'MMA',
          'MUTTHIDA MAJLIS-E-AMAL PAKISTAN': 'MMA',
          'MUTTAHIDA MAJLIS-E- AMAL PAKISTAN': 'MMA',
          'Muthida Majlis e Amal Pakistan': 'MMA',
          'Mutihida Majlis e Amal Pakistan': 'MMA',
          'M.M.A' : 'MMA',
          'Muttahida Majlis-e-Amal Pakistan':'MMA',
          #
          'Mutahida Qaumi Movemebt Pakistan': 'MQM',
          'Muttahida Qaumi Movement Pakistan': 'MQM',
          # 
          'Tehreek Labbaik Pakistan': 'TLP',
          'Tehreek labbaik Pakistan': 'TLP',
          'Tehrik e Labbaik': 'TLP',
          'Tahreek Labbaik pakistan': 'TLP',
          'Tehreek e Labbaik Pakistan': 'TLP',
          'Tehrek e labbaik Pakistan' : 'TLP',
          'Tehrik e Labbaik Pakistan': 'TLP',
          'Tehrik e Labbaik': 'TLP',
          'Tehrik e Labbaik': 'TLP',
          'Tehreek e labbaik Pakistan':'TLP',
          'Tehreek-e-Labbaik Pakistan': 'TLP',
          'Tehreek e Labbaik Pakistan TLI ': 'TLP',
          #
          'Awami National Party': 'ANP',
          'Avvami National Party': 'ANP',
          #
          'Pak Sarzameen Party': 'PSP',
          'Pak SarZamen Party': 'PSP',
          #
          'Pakistan Muslim League': 'PML-Q',
          'PML -Q':'PML-Q',
          #
          'Balochistan National Party': 'BNP',
          'Balochistan National Party': 'BNP',
          #
          'Balochistan Awami Party': 'BAP',
          'Balochistan Awami Party': 'BAP',
          #
          'Pashtoonkhwa Milli Awami Party': 'PKMAP',
          'PashtoonKhwa Milli Awami party': 'PKMAP',
          'Pakhtoonkhwa Milli Awami Party ': 'PKMAP',
          'Pashtoonkhawa Milli Awami Party': 'PKMAP',
          'Pashtunkhwa Milli Awami Party ': 'PKMAP',
          # 
          'All Pakistan Muslim League': 'APML',
          #
          'Grand Democratic Allience': 'GDA',
          'G.D.A': 'GDA',
          #
          'Sindh United Party': 'SUP',
          #
          'Qaumi Watan Party': 'QWP',
          "Pakistan Muslim League (Z)":"PML-Z"
          
        }
    df_result_2018['results__party'].replace(replacements, inplace=True)
    
    return df_result_2018