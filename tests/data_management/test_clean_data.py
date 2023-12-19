import numpy as np
import pandas as pd
import pytest
import os
from ge_effects_of_subsidies.config import TEST_DIR, FARM_SUBSIDY_DATA_PATH, BLD
from ge_effects_of_subsidies.data_management import clean_data
from ge_effects_of_subsidies.utilities import read_yaml
from ge_effects_of_subsidies.data_management.clean_data import _get_all_file_data_paths, _combine_all_data_into_df, _extract_longitude, _generate_zipcode_column, _extract_latitude




def test_get_all_file_data_paths_correct_number_datasets():
    data_paths = _get_all_file_data_paths(FARM_SUBSIDY_DATA_PATH)
    assert len(data_paths) == 8

def test_combine_all_data_into_df_correct_shape():
    file_paths = _get_all_file_data_paths(FARM_SUBSIDY_DATA_PATH)
    df = _combine_all_data_into_df(file_paths)
    assert df.shape[1] ==  21


def test_generate_zipcode_column():
    # Create a DataFrame with sample data
    data = {'recipient_name': ['Schmidt, Hans', 'Meier, Max', 'Struck-Sievers, Joachim'], 'recipient_address': ['Dresden, DE-01067', 'Berlin, DE-10117', 'Dresden, DE#BEZUG']}
    df = pd.DataFrame(data)

    # Generate the zipcode column
    zipcodes = _generate_zipcode_column(df)

    # Assert that the correct zipcode is assigned to the correct recipient
    assert zipcodes[0] == '01067'
    assert zipcodes[1] == '10117'
    assert zipcodes[2] == '16244'


def test_extract_latitude_expected_output():
    zipcodes_test = ["94105", "94043", "94301"]
    actual = _extract_latitude(zipcodes_test)
    expected = [37.78846925026178, 22.368609, 47.79655491375995]
    assert np.isclose(np.array(expected), np.array(actual)).all()



#Remember this test and implement it later!
#def test_amount_vs_amount_original():
#    data = pd.read_pickle(BLD / "python" / "data" / "data_farm_subsidy_clean.pkl")
#    amount_original = data.query("currency == 'EUR'")["amount_original"]
#    amount_converted = data.query("currency == 'EUR'")["amount"]
#    assert np.isclose(amount_original, amount_converted).all()


#These were only the example tests

# @pytest.fixture()
# def data():
#     return pd.read_csv(TEST_DIR / "data_management" / "data_fixture.csv")


# @pytest.fixture()
# def data_info():
#     return read_yaml(TEST_DIR / "data_management" / "data_info_fixture.yaml")

# def test_clean_data_drop_columns(data, data_info):
#     data_clean = clean_data(data, data_info)
#     assert not set(data_info["columns_to_drop"]).intersection(set(data_clean.columns))


# def test_clean_data_dropna(data, data_info):
#     data_clean = clean_data(data, data_info)
#     assert not data_clean.isna().any(axis=None)


# def test_clean_data_categorical_columns(data, data_info):
#     data_clean = clean_data(data, data_info)
#     for cat_col in data_info["categorical_columns"]:
#         renamed_col = data_info["column_rename_mapping"].get(cat_col, cat_col)
#         assert data_clean[renamed_col].dtype == "category"


# def test_clean_data_column_rename(data, data_info):
#     data_clean = clean_data(data, data_info)
#     old_names = set(data_info["column_rename_mapping"].keys())
#     new_names = set(data_info["column_rename_mapping"].values())
#     assert not old_names.intersection(set(data_clean.columns))
#     assert new_names.intersection(set(data_clean.columns)) == new_names


# def test_convert_outcome_to_numerical(data, data_info):
#     data_clean = clean_data(data, data_info)
#     outcome_name = data_info["outcome"]
#     outcome_numerical_name = data_info["outcome_numerical"]
#     assert outcome_numerical_name in data_clean.columns
#     assert data_clean[outcome_name].dtype == "category"
#     assert data_clean[outcome_numerical_name].dtype == np.int8
