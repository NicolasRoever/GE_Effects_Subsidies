"""All the general configuration of the project."""
from pathlib import Path

SRC = Path(__file__).parent.resolve()
BLD = SRC.joinpath("..", "..", "bld").resolve()

TEST_DIR = SRC.joinpath("..", "..", "tests").resolve()
PAPER_DIR = SRC.joinpath("..", "..", "paper").resolve()

FARM_SUBSIDY_DATA_PATH = SRC / "data" / "FarmSubsidyData" / ""

CLEANED_DATA_PATH = BLD / "python" / "data" / "data_farm_subsidy_clean.pkl"

GERMAN_GDP_DATA_PATH = SRC / "data" / "Macro_Data" / "germany-gdp-gross-domestic-product.csv"

GROUPS = ["marital_status", "qualification"]

MAPBOX_TOKEN =  "pk.eyJ1Ijoibmljb3JvZXZlciIsImEiOiJjbHFjZmgwNmYwMWN5MmtrMnB0cXFzeHZxIn0.k_McexSZGPeL8QmDeqEDeg"

__all__ = ["BLD", "SRC", "TEST_DIR", "GROUPS"]
