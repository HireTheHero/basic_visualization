from itertools import combinations
from typing import Dict, List, Union

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def plot_ctgry_vs_ctgries(
    data: pd.DataFrame,
    target_cols: List[str],
    category_cols: List[str],
    horizontal_spacing: Union[int, float] = 0.2,
    agg_col: str = "colname",
    agg_type: str = "sum"
):
    for tgt_col in target_cols:
        fig = make_subplots(
            1,
            len(category_cols),
            horizontal_spacing=horizontal_spacing,
            subplot_titles=category_cols,
        )
        for idx, ctgry_col in enumerate(category_cols):
            data_ct = pd.crosstab(data[tgt_col], data[ctgry_col], normalize="columns", values=data[agg_col], aggfunc=agg_type)
            fig.add_trace(go.Heatmap(z=data_ct), 1, idx + 1)
        fig.update_traces(showscale=False)
        fig.update_layout(title=f"{tgt_col} vs {category_cols}")
        fig.show()
    return


def decide_tile(
    data: pd.DataFrame,
    tiles: List[Union[int, float]],
):
    df_tile = data.quantile(tiles)
    out = {}
    print(f"Selected quantiles: {tiles}")
    for col in df_tile.columns:
        print(df_tile[col].tolist())
        tile_l = input("Lower fill: ")
        tile_u = input("Upper fill: ")
        fill_l = df_tile.loc[float(tile_l), col]
        fill_u = df_tile.loc[float(tile_u), col]
        out[col] = [fill_l, fill_u]
    return out

def show_tile(
    data: pd.DataFrame,
    tiles: List[Union[int, float]] = [
        0,
        0.01,
        0.02,
        0.03,
        0.05,
        0.25,
        0.5,
        0.75,
        0.95,
        0.97,
        0.98,
        0.99,
        1,
    ],
):
    df_tile = data.quantile(tiles)
    return df_tile


def fill_tile(
    data: pd.DataFrame,
    tiles: List[Union[int, float]],
    is_interactive: bool = False,
    fills_given: Dict[str, List[float]] = None
):
    if is_interactive:
        fills = decide_tile(data, tiles)
    else:
        fills = fills_given
    out = data.copy()
    for col in data.columns:
        out.loc[out[col] < fills[col][0], col] = fills[col][0]
        out.loc[out[col] > fills[col][1], col] = fills[col][1]
    return out


def plot_filled_dist2d(
    data: pd.DataFrame,
    cols: List[str],
    tiles: List[Union[int, float]] = [
        0,
        0.01,
        0.02,
        0.03,
        0.05,
        0.95,
        0.97,
        0.98,
        0.99,
        1,
    ],
    is_interactive: bool = False,
    fills_given: Dict[str, List[float]] = None
):
    df_filled = fill_tile(data[cols], tiles, is_interactive, fills_given)
    col_combs = combinations(cols, 2)
    for comb in col_combs:
        fig = px.density_heatmap(
            df_filled,
            x=comb[0],
            y=comb[1],
            marginal_x="histogram",
            marginal_y="histogram",
        )
        fig.show()
    return

def summarize_bin(data: pd.DataFrame, cols: List[str], num_bins: int = 100):
    def _bin_col(data: pd.DataFrame, bin_col:str, num_bins=num_bins):
        data[f"{bin_col}_bin{num_bins}"] = pd.qcut(data[bin_col], num_bins, labels=False)
        return out

    out = data.copy()
    for col in cols:
        out = _bin_col(out, col)

    return out
    