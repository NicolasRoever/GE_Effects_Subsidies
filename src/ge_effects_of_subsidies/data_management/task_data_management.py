"""Tasks for managing the data."""

from pathlib import Path

import pandas as pd
import pdbp 

from ge_effects_of_subsidies.config import BLD, SRC, FARM_SUBSIDY_DATA_PATH, GERMAN_GDP_DATA_PATH
from ge_effects_of_subsidies.data_management.clean_data import clean_data, _get_all_file_data_paths, _combine_all_data_into_df, _clean_farm_subsidy_data_for_analysis, _clean_german_gdp_data
from ge_effects_of_subsidies.utilities import read_yaml




def task_clean_farm_subsidy_data(
    produces=BLD / "python" / "data" / "data_farm_subsidy_clean.pkl"):  

    file_paths = _get_all_file_data_paths(FARM_SUBSIDY_DATA_PATH)
    df = _combine_all_data_into_df(file_paths)
    analysis_df = _clean_farm_subsidy_data_for_analysis(df)
    analysis_df.to_pickle(produces)


def task_clean_gdp_data(depends_on= GERMAN_GDP_DATA_PATH, 
    produces= BLD / "python" / "data" / "data_gdp_clean.pkl"):  

    data = pd.read_csv(depends_on,  skiprows=16)
    analysis_df = _clean_german_gdp_data(data)
    analysis_df.to_pickle(produces)



#This was only the example task code
    
# clean_data_deps = {
#     "scripts": Path("clean_data.py"),
#     "data_info": SRC / "data_management" / "data_info.yaml"
# }

    
# def task_clean_data_python(
#     depends_on=clean_data_deps,
#     produces=BLD / "python" / "data" / "data_clean.csv",
# ):
#     """Clean the data (Python version)."""
#     data_info = read_yaml(depends_on["data_info"])
#     data = pd.read_csv(depends_on["data"])
#     data = clean_data(data, data_info)
#     data.to_csv(produces, index=False)