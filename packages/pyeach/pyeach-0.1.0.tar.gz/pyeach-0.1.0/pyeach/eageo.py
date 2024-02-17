"""
eageo provides functions for loading shapefile data and constructing folium maps.
"""

import contextily as cx
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pygris import tracts, block_groups, blocks
from folium import Choropleth, FeatureGroup, Marker, Icon
from importlib.resources import files
from pyeach.extras.loaders import read_txt


def select_geo_data(df, geoid, col, geocol="GEOID", repl="Unknown"):
    """Select the value associated with the geoid and return it as a string if it exists, otherwise returns replacement.

    Args:
        df (pd.DataFrame): Dataframe of descriptive variables linked to geometry.
        geoid (str): ID of geometry to match.
        col (str): Column name of desired data values.
        geocol (str, optional): Column name of geometry IDs. (Defaults to "GEOID")
        repl (str, optional): Replacement for unmatched values. (Defaults to "Unknown")

    Returns:
        str: A string of the value at the geometry ID. 
    """
    try:
        c = str(df[df[geocol]==geoid][col].values[0])
    except IndexError:
        c = repl
    return c


def add_choro(df, col, name, geodata, geocol="GEOID", opacity=0.7, colormap="RdBu_r", bins=10):
    """Generate a folium choropleth layer that can be added to folium map.

    Args:
        df (pd.DataFrame): Dataframe containing geo location IDs and numeric values to determine shape colors.
        col (str): Column name to assign colors from.
        name (str): Name of the folium layer.
        geodata (dict): Shape data to construct boundaries.
        geocol (str, optional): Column name to key on (must match in df and geodata). Defaults to "GEOID".
        opacity (float, optional): Color fill opacity. Defaults to 0.7.
        colormap (str, optional): Color scale to use. Defaults to "RdBu_r".
        bins (int, optional): Number of bins to create stepwise gradient. Defaults to 10.

    Returns:
        folilum.Choropleth: Choropleth layer that can added to a folium map.
    """
    chmap = Choropleth(
        name = name,
        geo_data = geodata,
        data = df,
        columns = [geocol, col],
        key_on=f"properties.{geocol}",
        legend_name=name,
        fill_opacity=opacity,
        fill_color = colormap,
        bins = bins
    )
    return chmap


def add_markers(name, data, prefix, icon, icon_color, feature_name="Name", lat_name="lat", lon_name="lon"):
    """Add point markers to a folium map.

    Args:
        name (str): Name of the marker(s).
        data (pd.DataFrame): Coordinates DataFrame and location names.
        prefix (str): Prefix for icon.
        icon (str): Icon description.
        icon_color (str): Color of icon.
        feature_name (str, optional): Column name of location names. Defaults to "Name".
        lat_name (str, optional): Column name of latitude values. Defaults to "lat".
        lon_name (str, optional): Column name of longitude values. Defaults to "lon".

    Returns:
        folium.Marker: Marker(s) to add to a folium map.
    """
    markers = FeatureGroup(name = name, overlay = True)
    for i in data.index:
        site = data.loc[i, feature_name]
        lat = float(data.loc[i, lat_name])
        lon = float(data.loc[i, lon_name])

        Marker(
            location=[lat, lon],
            popup=site,
            icon=Icon(prefix=prefix, icon=icon, color = icon_color)
        ).add_to(markers)

    return markers

def map_result(map_df, y, map_size=10):
    """Generate a choropleth map based on a GeoDataFrame.

    Args:
        map_df (gpd.GeoDataFrame): The GeoDataFrame containing geographical data.
        y (str): The column name for the variable to be visualized.
        map_size (int, optional): The size of the resulting map. Defaults to 10.
    """
    map_df = gpd.GeoDataFrame(map_df, crs= {"init": "epsg:4326"}, geometry="geometry")#, crs=4326)
    map_df = map_df.to_crs('EPSG:3857')
    fig, ax = plt.subplots(figsize = (map_size, map_size))
    map_df.plot(
        ax=ax,
        figsize=(5, 5),
        column=y,
        legend=True,
        legend_kwds={'shrink': 0.3},
        alpha=0.75,
    )
    cx.add_basemap(ax, source=cx.providers.Stamen.TonerLabels)
    cx.add_basemap(ax, source=cx.providers.Stamen.TonerLite)
    # Remove axis
    ax.set_axis_off()
    ax.set_xlim(map_df.total_bounds[0], map_df.total_bounds[2])
    ax.set_ylim(map_df.total_bounds[1], map_df.total_bounds[3])
    plt.show()

def nc_va_geos(agg):
    """Obtain geo data from pygris for North Carolina (NC) and Virginia (VA).

    Args:
        agg (str): The level of geographical aggregation, options: "tract", "block", "block_groups".

    Returns:
        gpd.GeoDataFrame: A GeoDataFrame containing the combined geographical data for NC and VA.
    """
    if agg=="tract":
        geo_agg = tracts
    elif agg=="block":
        geo_agg = blocks
    elif agg=="block_groups":
        geo_agg = block_groups
    nc = geo_agg(state = "NC")
    va = geo_agg(state = "VA")
    nc_va = pd.concat([nc, va]).drop_duplicates(subset=["GEOID"])
    nc_va["area"] = nc_va.geometry.area

    return nc_va


def locations(group):
    """Get the coordinates of important Cone Health locations. Options include ED/UC departments, hospitals, PCP, 
    aggregate housing, congregational nursing program, community care, and community food locations.

    Args:
        group (str): Indicator for which group of locations to load. Options include ['ed_uc', 'hospitals', 'pcp', 
        'agg_housing', 'cnp', 'comm_care', 'comm_food'].

    Returns:
        pd.DataFrame: DataFrame of location coordinates.
    """

    groups = {"ed_uc": "ed_uc_locations.txt", 
              "hospitals": "hospital_locations.txt", 
              "pcp": "pcp_locations.txt", 
              "agg_housing": "aggregate_housing_locations.txt", 
              "cnp": "cnp_locations.txt",
              "comm_care": "comm_care_locations.txt",
              "comm_food": "comm_food_locations.txt"}
    assert group in groups, f"group must be one of {list(groups.keys())}"
    
    data_text = files("pyeach.data").joinpath(groups[group])
    df = read_txt(data_text)

    return df