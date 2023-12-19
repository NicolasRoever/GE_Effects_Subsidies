import plotly.express as px
import pandas as pd


def _create_subsidy_map_2014(data, MAPBOX_TOKEN):
    px.set_mapbox_access_token(MAPBOX_TOKEN)

    data_filtered = data[
    (data["year"] == 2014)]

    # Extract the NUTS 3 region names from the 'nuts_3' column
    nuts3_names = list(data_filtered["nuts_3"].unique())

    # Create a dictionary to store the latitude, longitude, and subsidy data for each NUTS 3 region
    nuts3_names = list(data_filtered["nuts_3"].unique())

    subsidy_data = {}
    for nuts3_name in nuts3_names:
        latitude = data_filtered[data_filtered["nuts_3"] == nuts3_name]["latitude"].mean()
        longitude = data_filtered[data_filtered["nuts_3"] == nuts3_name]["longitude"].mean()
        total_subsidy = data_filtered[data_filtered["nuts_3"] == nuts3_name]["amount_euro"].sum()

        subsidy_data[nuts3_name] = {"latitude": latitude, "longitude": longitude, "subsidy": total_subsidy}

    subsidy_data_df = pd.DataFrame.from_dict(subsidy_data, orient="index", columns=["latitude", "longitude", "subsidy"])

    fig = px.scatter_mapbox(subsidy_data_df, lat="latitude", lon="longitude", color="subsidy", size="subsidy",
                color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=4)

    return fig


def _plot_subsidies_per_year(data):
    subsidies_by_year = data.groupby("year")["amount_euro"].sum()
    fig = px.line(subsidies_by_year, x=subsidies_by_year.index, y="amount_euro")
    return fig



def _plot_subsidies_per_gdp_per_year(data, gdp_data):
    subsidies_by_year = data.groupby("year")["amount_euro"].sum()
    subsidy_by_year_df =  pd.DataFrame(subsidies_by_year).reset_index()
    subsidy_by_year_df_merge = subsidy_by_year_df.merge(gdp_data, on="year", how="left")
    subsidy_by_year_df_merge["subsidy_per_gdp"] = subsidy_by_year_df_merge["amount_euro"] / subsidy_by_year_df_merge["gdp"]


    fig = px.line(subsidy_by_year_df_merge, x="year", y="subsidy_per_gdp")
    return fig
