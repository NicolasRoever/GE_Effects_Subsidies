"""Tasks running the core analyses."""

from pathlib import Path

import pandas as pd
import pytask

from ge_effects_of_subsidies.analysis.model import fit_logit_model, load_model
from ge_effects_of_subsidies.analysis.predict import predict_prob_by_age
from ge_effects_of_subsidies.config import BLD, GROUPS, SRC, CLEANED_DATA_PATH, MAPBOX_TOKEN
from ge_effects_of_subsidies.utilities import read_yaml
from ge_effects_of_subsidies.analysis.descriptive_analysis import _create_subsidy_map_2014, _plot_subsidies_per_year



def task_plot_subsidies_2014(depends_on = CLEANED_DATA_PATH, 
                             produces = BLD / "figures" / "subsidies_2014_map.png"):
    
    data = pd.read_pickle(depends_on)
    figure = _create_subsidy_map_2014(data, MAPBOX_TOKEN)
    figure.write_image(produces)

def task_plot_subsidies_per_year(depends_on = CLEANED_DATA_PATH, 
                                 produces = BLD / "figures" / "subsidies_per_year.png"):
    
    data = pd.read_pickle(depends_on)
    figure = _plot_subsidies_per_year(data)
    figure.write_image(produces)



##Example Code

fit_model_deps = {
    "scripts": [Path("model.py"), Path("predict.py")],
    "data": BLD / "python" / "data" / "data_clean.csv",
    "data_info": SRC / "data_management" / "data_info.yaml",
}


def task_fit_model_python(
    depends_on=fit_model_deps,
    produces=BLD / "python" / "models" / "model.pickle",
):
    """Fit a logistic regression model (Python version)."""
    data_info = read_yaml(depends_on["data_info"])
    data = pd.read_csv(depends_on["data"])
    model = fit_logit_model(data, data_info, model_type="linear")
    model.save(produces)


for group in GROUPS:
    predict_deps = {
        "data": BLD / "python" / "data" / "data_clean.csv",
        "model": BLD / "python" / "models" / "model.pickle",
    }

    @pytask.task(id=group)
    def task_predict_python(
        group=group,
        depends_on=predict_deps,
        produces=BLD / "python" / "predictions" / f"{group}.csv",
    ):
        """Predict based on the model estimates (Python version)."""
        model = load_model(depends_on["model"])
        data = pd.read_csv(depends_on["data"])
        predicted_prob = predict_prob_by_age(data, model, group)
        predicted_prob.to_csv(produces, index=False)
