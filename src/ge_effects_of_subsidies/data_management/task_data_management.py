"""Tasks for managing the data."""

from pathlib import Path

import pandas as pd
import pdbp 

from ge_effects_of_subsidies.config import BLD, SRC, FARM_SUBSIDY_DATA_PATH
from ge_effects_of_subsidies.data_management.clean_data import clean_data, _get_all_file_data_paths, _combine_all_data_into_df
from ge_effects_of_subsidies.utilities import read_yaml

clean_data_deps = {
    "scripts": Path("clean_data.py"),
    "data_info": SRC / "data_management" / "data_info.yaml"
}




def task_clean_farm_subsidy_data(
    produces=BLD / "python" / "data" / "data_farm_subsidy_clean.csv"):  

    file_paths = _get_all_file_data_paths(FARM_SUBSIDY_DATA_PATH)
    df = _combine_all_data_into_df(file_paths)
    df.to_csv(produces, index=False)



#This was only the example task code
    
# def task_clean_data_python(
#     depends_on=clean_data_deps,
#     produces=BLD / "python" / "data" / "data_clean.csv",
# ):
#     """Clean the data (Python version)."""
#     data_info = read_yaml(depends_on["data_info"])
#     data = pd.read_csv(depends_on["data"])
#     data = clean_data(data, data_info)
#     data.to_csv(produces, index=False)