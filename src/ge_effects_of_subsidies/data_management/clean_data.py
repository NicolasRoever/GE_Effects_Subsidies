"""Function(s) for cleaning the data set(s)."""

import pandas as pd
import os
from pathlib import Path
import pgeocode

import numpy as np



def _clean_farm_subsidy_data_for_analysis(df):
    data = pd.DataFrame()
    data['country'] = df['country'].astype('category')
    data['year'] = df['year'].astype('int16')
    data['recipient_id'] = df["recipient_id"].astype('category')
    data['recipient_name'] = df["recipient_name"].astype('str')
    data["scheme_id"] = df["scheme_id"].astype('category')
    data["amount_euro"] = df["amount_original"].astype('float32')
    data["nuts_3"] = df["nuts3"].astype('category')
    data["zipcode"] = _generate_zipcode_column(df)
    data["longitude"] = _extract_longitude(data["zipcode"])
    data["latitude"] = _extract_latitude(data["zipcode"])


    return data
    


def _get_all_file_data_paths(directory):
    file_names = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    data_paths = [Path(directory / item) for item in file_names]
    return data_paths

def _extract_longitude(zipcodes, country = "de"):
    nomi = pgeocode.Nominatim(country)
    locations = nomi.query_postal_code(zipcodes)
    return locations["longitude"]


def _extract_latitude(zipcodes, country = "de"):
    nomi = pgeocode.Nominatim(country)
    locations = nomi.query_postal_code(zipcodes)
    return locations["latitude"]



def _combine_all_data_into_df(file_paths):
    dfs = []

    for file_path in file_paths:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path)

        # Append the DataFrame to the combined_df
        dfs.append(df)

    combined_df = pd.concat(dfs, ignore_index=True)

    return combined_df

def _generate_zipcode_column(df):
    zipcodes = _extract_zipcode(df['recipient_address'])
    #There is a mistake in the coding of one guy
    mistake_indedx = df[df['recipient_name'] == 'Struck-Sievers, Joachim'].index
    zipcodes[mistake_indedx] = '16244'
    return zipcodes

   
def _extract_zipcode(address):
    return address.str.extract('(\d+)', expand=False)



#####################################################################################################################
#####################################################################################################################
#This was only the example code


def clean_data(data, data_info):
    """Clean data set.

    Information on data columns is stored in ``data_management/data_info.yaml``.

    Args:
        data (pandas.DataFrame): The data set.
        data_info (dict): Information on data set stored in data_info.yaml. The
            following keys can be accessed:
            - 'outcome': Name of dependent variable column in data
            - 'outcome_numerical': Name to be given to the numerical version of outcome
            - 'columns_to_drop': Names of columns that are dropped in data cleaning step
            - 'categorical_columns': Names of columns that are converted to categorical
            - 'column_rename_mapping': Old and new names of columns to be renamend,
                stored in a dictionary with design: {'old_name': 'new_name'}
            - 'url': URL to data set

    Returns:
        pandas.DataFrame: The cleaned data set.

    """
    data = data.drop(columns=data_info["columns_to_drop"])
    data = data.dropna()
    for cat_col in data_info["categorical_columns"]:
        data[cat_col] = data[cat_col].astype("category")
    data = data.rename(columns=data_info["column_rename_mapping"])

    numerical_outcome = pd.Categorical(data[data_info["outcome"]]).codes
    data[data_info["outcome_numerical"]] = numerical_outcome

    return data