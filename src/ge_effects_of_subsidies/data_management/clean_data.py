"""Function(s) for cleaning the data set(s)."""

import pandas as pd
import os
from pathlib import Path

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


def _get_all_file_data_paths(directory):
    file_names = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    data_paths = [Path(directory / item) for item in file_names]
    return data_paths



def _combine_all_data_into_df(file_paths):
    dfs = []

    for file_path in file_paths:
        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path)

        # Append the DataFrame to the combined_df
        dfs.append(df)

    combined_df = pd.concat(dfs, ignore_index=True)

    return combined_df