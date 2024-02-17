import re
from copy import copy
from typing import Any, List, Tuple

import numpy as np
import pandas as pd
import plotly.graph_objs as go
from scipy.stats import gaussian_kde

from aixd.mlmodel.constants import colors

# Wrapper function for different basic plotly plots


def contour2d(fig: go.Figure, x: np.ndarray, y: np.ndarray, title: str = "", pos: Tuple[int, int] = (1, 1), **kwargs) -> go.Figure:
    """Wrapper for the plotly Histogram2dContour plot. The kwargs are passed to the plotly function."""
    return fig.add_trace(go.Histogram2dContour(x=x.flatten(), y=y.flatten(), colorscale="Blues", showscale=False, name=title, **kwargs), row=pos[0], col=pos[1])


def hist1d(fig: go.Figure, x: Any, title: str = "", pos: Tuple[int, int] = (1, 1), **kwargs) -> go.Figure:
    """Wrapper for the plotly Histogram plot. The kwargs are passed to the plotly function."""
    return fig.add_trace(go.Histogram(x=x, name=title, **kwargs), row=pos[0], col=pos[1])


def barplot(fig: go.Figure, x: Any, title: str = "", pos: Tuple[int, int] = (1, 1), **kwargs) -> go.Figure:
    """Wrapper for the plotly Bar plot. The kwargs are passed to the plotly function."""
    val, count = np.unique(x, return_counts=True)
    return fig.add_trace(go.Bar(x=val, y=count, name=title, **kwargs), row=pos[0], col=pos[1])


def hist2d(fig: go.Figure, x: Any, y: Any, title: str = "", pos: Tuple[int, int] = (1, 1), **kwargs) -> go.Figure:
    """Wrapper for the plotly Histogram2d plot. The kwargs are passed to the plotly function."""
    return fig.add_trace(go.Histogram2d(x=x, y=y, name=title, **kwargs), row=pos[0], col=pos[1])


def scatter2d(fig: go.Figure, x: Any, y: Any, title: str = "", pos: Tuple[int, int] = (1, 1), **kwargs) -> go.Figure:
    """Wrapper for the plotly Scatter plot. The kwargs are passed to the plotly function."""
    return fig.add_trace(go.Scatter(x=x, y=y, name=title, **kwargs), row=pos[0], col=pos[1])


# Helpers


def append_unit(name: str, unit: str) -> str:
    """
    Append a unit to a name. See unit_to_html(...) for the conversion of the unit to a string with HTML tags for subscripts and superscripts.
    """
    if unit is None:
        return name
    else:
        return f"{name} [{unit_to_html(unit)}]"


def unit_to_html(unit: str) -> str:
    """
    Convert a string representing a unit (e.g., km, km^2, m/s^2, etc.) to a string with HTML tags for subscripts and superscripts.

    Parameters
    ----------
    unit : str
        String representing a unit.

    Returns
    -------
    str
        String with HTML tags for subscripts and superscripts.

    Examples
    --------
    >>> unit_to_html("km")
    'km'
    >>> unit_to_html("km^2")
    'km<sup>2</sup>'
    >>> unit_to_html("m/s^2")
    'm/s<sup>2</sup>'

    """
    # Plotly (as opposed to matplotlib) does not support labels mixed with regular text and latex equations. It's only possible to enclose the entire label in a latex equation,
    # which results in a different font for text. As we only want to make it possible to use subscripts and superscripts, the corresponding HTML tags are used instead.
    # See https://plotly.com/python/LaTeX/ for more information.
    pattern = r"([a-zA-Z]+)([_^])([0-9a-zA-Z]+)"

    def replace(match):
        base = match.group(1)
        operator = match.group(2)
        exponent = match.group(3)

        if operator == "_":
            return f"{base}<sub>{exponent}</sub>"
        elif operator == "^":
            return f"{base}<sup>{exponent}</sup>"

    return re.sub(pattern, replace, unit)


# Other plots


def add_kde_trace(fig: go.Figure, data: Any, title: str, cumulative: bool = False, pos: Tuple[int, int] = (1, 1), with_mean=True, with_std=True, n_samples=None, **kwargs):
    """
    Adds a KDE trace to the given figure. If cumulative is True, the trace is a CDF, otherwise a PDF. The kwargs are passed to the Scatter plot. It, also, adds the mean and
    prediction interval, assuming a normal distribution, if with_mean and with_std are True, respectively.
    """
    data = np.asarray(data).astype(float).flatten()
    kde = gaussian_kde(data)

    n_samples = n_samples or (100 if cumulative else 1000)
    x = np.linspace(min(data), max(data), n_samples)

    # Compute sample values and add trace
    if cumulative:
        y = [kde.integrate_box_1d(-np.inf, val) for val in x]
        fig = scatter2d(fig, x, y, title=f"{title} (CDF)", mode="lines", pos=pos, **kwargs)
    else:
        y = kde.evaluate(x)
        fig = scatter2d(fig, x, y, title=f"{title} (PDF)", mode="lines", pos=pos, **kwargs)

    # Add mean and prediction interval
    mean, std = np.mean(data), np.std(data)
    vline_kwargs = dict(line_width=2, line_dash="dash", line_color="orangered", annotation_yanchor="bottom", annotation_xanchor="center", row=pos[0], col=pos[1])
    if with_mean:
        fig = fig.add_vline(
            x=mean,
            annotation_text=r"&mu;",
            **vline_kwargs,
        )
    if with_std:
        fig = fig.add_vline(x=mean + std, annotation_text="+\u03C3", **vline_kwargs)
        fig = fig.add_vline(x=mean - std, annotation_text="-\u03C3", **vline_kwargs)

    return fig


def attribute_obs_vs_pred(
    fig: go.Figure, obs: pd.DataFrame, pred: pd.DataFrame, errors: pd.DataFrame, cols: List[str], downsamp: int = 1, pos: Tuple[int, int] = (1, 1), legend: str = None
) -> go.Figure:
    """
    Plots observations vs. predictions as a scatter plot, while markers are colored according to the errors into five classes. If len(cols) > 1, the data is flattened.
    """
    obs = np.asarray(obs[cols])[::downsamp].flatten()
    pred = np.asarray(pred[cols])[::downsamp].flatten()
    errors = np.asarray(errors[cols])[::downsamp].flatten()

    num_categories = 5
    ranges = np.linspace(0, max(errors), num=num_categories + 1)
    ranges[0] = -np.inf

    # Define the color map for the categories
    color_list = ["#72C800", "#CFED00", "#F6DA00", "#E47E00", "#D22400"]
    color_map = dict(zip(ranges[1:], color_list))

    # Iterate trough error ranges in topdown fashion
    for low, high in zip(ranges[:-1][::-1], ranges[1:][::-1]):
        range_mask = (errors > low) & (errors <= high)

        fig = scatter2d(
            fig=fig,
            x=obs[range_mask],
            y=pred[range_mask],
            mode="markers",
            pos=pos,
            marker=dict(size=10, line=dict(width=2, color="white"), color=color_map[high]),
            customdata=errors[range_mask],
            hovertemplate="(%{x}, %{y}, %{customdata})",
            title=f"\u2264 {high:.2f}",
            legendgroup="ranges",
            legend=legend,
        )

    # Add a 45 degree line
    fig = scatter2d(
        fig,
        x=[np.min(obs), np.max(obs)],
        y=[np.min(obs), np.max(obs)],
        mode="lines",
        line=dict(color="orangered", width=2, dash="dash"),
        title="optimal",
        legendgroup="optimal",
        pos=pos,
        legend=legend,
    )

    fig.update_xaxes(title_text="Observed values", row=pos[0], col=pos[1])
    fig.update_yaxes(title_text="Predicted values", row=pos[0], col=pos[1])

    # Default legend options and position
    legend_options = {
        legend: dict(
            title="error",
            traceorder="grouped+reversed",
            groupclick="toggleitem",
            y=list(fig.select_yaxes(row=pos[0], col=pos[1]))[0].domain[1],
            x=list(fig.select_xaxes(row=pos[0], col=pos[1]))[0].domain[1] + 0.02,
            xref="paper",
            yref="paper",
            yanchor="top",
            xanchor="left",
        )
    }
    fig.update_layout(**legend_options)

    return fig


def errors_gen(fig, y_diff, y_diff_best, y_list, y_list_best, y_train, dobj, name_plot, pos, n_bins, offset=0.005, range_bins=None, **kwargs):
    # get absolute differences
    y_diff = np.abs(np.asarray(y_diff)).reshape(-1, 1)
    y_diff_best = np.abs(np.asarray(y_diff_best)).reshape(-1, 1)
    y_train = np.asarray(y_train).reshape(-1, 1)
    y_list = np.asarray(y_list).reshape(-1, 1)

    # Bins for x axis
    # Bins for x axis
    if range_bins is not None and dobj.type not in ["integer", "ordinal", "categorical"]:
        y_bins = np.linspace(range_bins[0], range_bins[1], n_bins + 1)
    else:
        y_bins = _bins_x_axis(dobj, y_train, n_bins)

    # Initialize list for mean and confidence intervals
    # Error per bin
    y_mean, y_conf, y_ids = _list_mean_conf(y_bins, y_diff, y_list, quantile=0.25)
    y_mean, y_conf = np.asarray(y_mean), np.asarray(y_conf)
    y_conf_rel = np.abs(y_conf.transpose() - y_mean)

    y_mean_best, y_conf_best, y_ids = _list_mean_conf(y_bins, y_diff_best, y_list_best, quantile=0.25)
    y_mean_best, y_conf_best = np.asarray(y_mean_best), np.asarray(y_conf_best)
    y_conf_rel_best = np.abs(y_conf_best.transpose() - y_mean_best)

    # plot losses
    n_per_bin = int(len(y_diff) / n_bins)
    fig = add_trace_error(fig, y_ids, y_mean, y_conf_rel, "de", "design error {}/{}".format(n_per_bin, n_per_bin), offset=offset, pos=pos, yaxis=2, **kwargs)

    n_per_bin_best = int(len(y_diff_best) / n_bins)
    fig = add_trace_error(fig, y_ids, y_mean_best, y_conf_rel_best, "de_s", "design error {}/{}".format(n_per_bin_best, n_per_bin), offset=offset, pos=pos, yaxis=2, **kwargs)

    # Update primary and secondary y-axes
    update_yaxis(fig, showgrid=False, zeroline=False, visible=False, row=pos[0], col=pos[1], yaxis=1)
    update_yaxis(
        fig,
        title_text="design error",
        side="left",
        range=[0, np.max(y_mean + y_conf_rel[0].tolist()) + 0.05],
        titlefont=dict(color=colors["de"]["main"]),
        row=pos[0],
        col=pos[1],
        yaxis=2,
    )

    return fig


def attribute_errors(fig, x_diff, y_diff, y_list, y_train, dobj, name_plot, cols, pos, n_bins, offset=0.005, range_bins=None, **kwargs):
    # get absolute differences
    x_diff = np.abs(np.asarray(x_diff)).mean(axis=1).reshape(-1, 1)
    y_diff_attr = np.abs(np.asarray(y_diff[cols])).reshape(-1, 1)
    y_train = np.asarray(y_train[cols]).reshape(-1, 1)
    y_list = np.asarray(y_list[cols]).reshape(-1, 1)

    # Bins for x axis
    if range_bins is not None and dobj.type not in ["integer", "ordinal", "categorical"]:
        y_bins = np.linspace(range_bins[0], range_bins[1], n_bins + 1)
    else:
        y_bins = _bins_x_axis(dobj, y_train, n_bins)

    # Initialize list for mean and confidence intervals
    # Error per bin
    x_mean, x_conf, y_ids = _list_mean_conf(y_bins, x_diff, y_list, quantile=0.25)
    y_mean, y_conf, y_ids = _list_mean_conf(y_bins, y_diff_attr, y_list, quantile=0.25)

    # get numpy arrays
    x_mean, y_mean = np.asarray(x_mean), np.asarray(y_mean)
    x_conf, y_conf = np.asarray(x_conf), np.asarray(y_conf)

    # get relative confidence intervals
    x_conf_rel = np.abs(x_conf.transpose() - x_mean)
    y_conf_rel = np.abs(y_conf.transpose() - y_mean)

    # plot losses
    fig = add_trace_error(fig, y_ids, x_mean, x_conf_rel, "x_err", "x error (overall)", offset=offset, pos=pos, yaxis=2, **kwargs)
    fig = add_trace_error(fig, y_ids, y_mean, y_conf_rel, "y_err", f"y error ({name_plot})", offset=offset, pos=pos, yaxis=3, **kwargs)

    # Update primary and secondary y-axes
    update_yaxis(fig, showgrid=False, zeroline=False, visible=False, row=pos[0], col=pos[1], yaxis=1)
    update_yaxis(
        fig,
        title_text="x error",
        side="left",
        range=[0, np.max(x_mean + x_conf_rel[0].tolist()) + 0.05],
        titlefont=dict(color=colors["x_err"]["main"]),
        row=pos[0],
        col=pos[1],
        yaxis=2,
    )
    update_yaxis(
        fig,
        title_text="y error",
        side="right",
        range=[0, np.max(y_mean + y_conf_rel[0].tolist()) + 0.05],
        showgrid=False,
        zeroline=False,
        titlefont=dict(color=colors["y_err"]["main"]),
        row=pos[0],
        col=pos[1],
        yaxis=3,
    )

    return fig


def add_trace_error(fig, y_ids, y_mean, y_conf_rel, str_color, name_p, offset=0.005, pos=(1, 1), yaxis=1, **kwargs):
    """Helper function to add the error trace."""
    add_trace(
        fig,
        go.Scatter(
            x=(np.asarray(y_ids) + offset).tolist(),
            y=y_mean.tolist(),
            name=name_p,
            line=dict(color=colors[str_color]["main"], width=5),
            error_y=dict(type="data", symmetric=False, array=y_conf_rel[0].tolist(), arrayminus=y_conf_rel[1].tolist(), color=colors[str_color]["main"], thickness=3, width=3),
            marker=dict(color=colors[str_color]["sec"], line=dict(width=2, color="white"), size=15),
            **kwargs,
        ),
        row=pos[0],
        col=pos[1],
        yaxis=yaxis,
    )
    return fig


def add_density(fig, data, dobj, names, name_plot, cols, pos, opacity=0.5, downsamp=2, **kwargs):
    """Helper function to add density distributions."""
    for i, split in enumerate(data):
        fig = dobj.plot_distrib(
            fig, split, cols, name_plot="{} {} data".format(name_plot, names[i]), pos=pos, downsamp=downsamp, marker=dict(color=colors["data"][names[i]]), **kwargs
        )

    fig.update_layout(barmode="overlay", paper_bgcolor="white")
    fig.update_traces(opacity=opacity, histnorm="probability density", bingroup=0.1, selector=dict(type="histogram"), row=pos[0], col=pos[1])
    return fig


def _list_mean_conf(y_bins, x_diff, y_list, quantile=0.25):
    # initialise lists
    y_ids = []
    x_mean, x_conf = [], []
    for j, y_bin in enumerate(y_bins[:-1]):
        # calculate errors for given bin
        x_errors = x_diff[(y_bins[j] <= y_list) & (y_list < y_bins[j + 1])]
        y_ids.append(y_bins[j] + (y_bins[j + 1] - y_bins[j]) / 2)

        # check for empty lists
        if len(x_errors) == 0:
            x_mean.append(np.nan), x_conf.append((np.nan, np.nan))
        else:
            x_mean.append(np.mean(x_errors))
            x_conf.append((np.quantile(x_errors, quantile), np.quantile(x_errors, 1 - quantile))),

    return x_mean, x_conf, y_ids


def _bins_x_axis(dobj, y_train, n_bins=10):
    if dobj.type in ["integer", "ordinal", "categorical"]:
        y_bins_aux = np.unique(y_train, return_counts=False)
        n_bins = len(y_bins_aux)
        y_bins_aux = np.concatenate([[-y_bins_aux[1] + 2 * y_bins_aux[0]], y_bins_aux, [-y_bins_aux[-2] + 2 * y_bins_aux[-1]]])
        y_bins = (y_bins_aux[1:] + y_bins_aux[:-1]) / 2
    else:
        y_bins = np.linspace(y_train.min(), y_train.max(), n_bins + 1)
    return y_bins


def add_bottom_top(fig: go.Figure, data: Any, bottom: float = None, top: float = None, pos: Tuple[int, int] = (1, 1)) -> go.Figure:
    """Adds two percentile (bottom and top) as vertical lines."""
    # Sort data
    data = np.asarray(data).flatten()
    data_sorted = data[data.argsort()][3:-3]

    # add percentage lines
    percentiles = [p for p in [bottom, top] if p is not None]
    for p in percentiles:
        vline_x = data_sorted[int(p * len(data_sorted))]

        # There is a bug in add_vline(...) when the axis of the figure has a categorical type
        # We apply the workaround discussed in https://github.com/plotly/plotly.py/issues/3065#issuecomment-1292583256 by combining add_vline(...) and add_annotation(...)
        fig.add_vline(x=vline_x, line_width=2, line_dash="dash", line_color="orangered", row=pos[0], col=pos[1])
        fig.add_annotation(x=vline_x, text=f"{int(p * 100)}%", row=pos[0], col=pos[1], y=1, yref="y domain", xanchor="left", yanchor="top", showarrow=False)

    return fig


# Helper functions tp extend plotly.Figure with subplots to arbitrary number of secondary y-axes


def get_subplot_size(fig: go.Figure) -> Tuple[int, int]:
    """Returns the number of rows and columns of the subplots in the given figure."""
    grid = fig._validate_get_grid_ref()  # this is the only way to get the number of rows and columns of the figure
    n_rows, n_cols = len(grid), len(grid[0])
    return n_rows, n_cols


def get_n_subplots(fig: go.Figure) -> int:
    """Returns the number of subplots in the given figure."""
    n_rows, n_cols = get_subplot_size(fig)
    return n_rows * n_cols


def make_secondary_yaxis(fig: go.Figure, n_secondary_y: int) -> go.Figure:
    """
    Adds multiple secondary y-axes to every subplot in the given figure. It assumes that the figure was created with plotly.subplots.make_subplots(...), and encodes
    the axes as follows:

        * The n_rows x n_cols axes are the primary y-axes. I.e., yaxis, yaxis2, ..., yaxis(n_rows x n_cols).
        * The next n_rows x n_cols axes are the first secondary y-axes of the subplots. I.e., yaxis(n_rows x n_cols + 1), yaxis(n_rows x n_cols + 2), ...,
          yaxis(2 x n_rows x n_cols).
        * The next n_rows x n_cols axes are the second secondary y-axes of the subplots. I.e., yaxis(2 x n_rows x n_cols + 1), yaxis(2 x n_rows x n_cols + 2), ...,
          yaxis(3 x n_rows x n_cols).
        * Etc.

    Parameters
    ----------
    fig : go.Figure
        The figure to add the secondary y-axes to.
    n_secondary_y : int
        The number of secondary y-axes to add to every subplot.

    Returns
    -------
    go.Figure
        The figure with the added secondary y-axes.

    """
    n_plots = get_n_subplots(fig)
    y_axes = list(fig.select_yaxes())

    if len(y_axes) != n_plots:
        raise ValueError("The number of y-axes must equal the number of subplots, before adding secondary y-axes.")

    secondary_axis_options = dict()
    for i in range(n_secondary_y):
        for j, yaxis in enumerate(y_axes):
            secondary_axis_options |= {f"yaxis{n_plots + i * n_plots + j + 1}": dict(anchor=f"x{j + 1}", overlaying=f"y{j + 1}", side="right", domain=copy(yaxis.domain))}
    fig = fig.update_layout(**secondary_axis_options)

    assert len(list(fig.select_yaxes())) == (n_secondary_y + 1) * n_plots
    return fig


def update_yaxis(fig: go.Figure, row: int = 1, col: int = 1, yaxis: int = 1, **kwargs) -> go.Figure:
    """
    Updates the y-axis of the subplot at the given row and column. If yaxis > 1, the y-axis is a secondary y-axis. Otherwise, it is the primary y axis.

    Parameters
    ----------
    fig : go.Figure
        The figure to update.
    row : int, optional, default=1
        The row of the subplot.
    col : int, optional, default=1
        The column of the subplot.
    yaxis : int, optional, default=1
        The index of the y-axis.
    **kwargs
        The arguments the y-axis is updated with.
    """
    if yaxis > 1:
        y_axis_key = f"yaxis{get_yaxis_id(fig, row, col, yaxis)}"
        fig.layout[y_axis_key].update(**kwargs)
    else:
        fig.update_yaxes(**kwargs, row=row, col=col)
    return fig


def get_yaxis_id(fig: go.Figure, row: int, col: int, yaxis: int = 1) -> int:
    """
    Returns the key of the y-xis of the subplot at the given row and column. If yaxis > 1, the y-axis is a secondary y-axis. Otherwise, it is the primary y-axis.
    Raises a ValueError in the following cases:

        * The number of y-axes is not a multiple of the number of subplots.
        * The subplot at the given row and column has not enough y-axes to access the y-axis at the given index.
        * The figure was not created with plotly.subplots.make_subplots(...)

    The first two cases can be avoided by using the make_secondary_yaxis(...) function to add enough secondary y-axes to the figure, after creating the figure with
    plotly.subplots.make_subplots(...).

    Parameters
    ----------
    fig : go.Figure
        The figure to get the y-axis key from.
    row : int
        The row of the subplot.
    col : int
        The column of the subplot.
    yaxis : int, optional, default=1
        The index of the y-axis.

    Returns
    -------
    int
        The key of the y-axis.
    """

    if yaxis < 1:
        raise ValueError("The y axis index must be greater than or equal to 1.")

    n_rows, n_cols = get_subplot_size(fig)
    n_plots = get_n_subplots(fig)
    n_yaxes = len(list(fig.select_yaxes()))

    if n_yaxes % n_plots != 0:
        raise ValueError("The number of y axes must be a multiple of the number of subplots. Make sure that you used make_secondary_yaxis(...) to add enough secondary y-axes.")

    if yaxis > n_yaxes // n_plots:
        raise ValueError(
            f"The subplot at row {row} and column {col} has only {n_yaxes // n_plots} y-axes, but you are trying to access the {yaxis}th y-axis. "
            f"Make sure to use make_secondary_yaxis(...) to add enough secondary y-axes."
        )

    # Compute the index of the requested y-axis of the subplot at the given row and column
    key = (row - 1) * n_cols + col + (yaxis - 1) * n_plots
    return key


def add_trace(fig: go.Figure, trace, row: int = 1, col: int = 1, yaxis: int = 1) -> go.Figure:
    """
    Adds the given trace to the subplot at the given row and column, and to specifed y-axes. If yaxis == 1, the trace is added to the primary y-axis, and equals the add_trace(...)
    method of plotly.graph_objs.Figure. If yaxis > 1, the trace is added to the indicated secondary y-axis.

    Parameters
    ----------
    fig : go.Figure
        The figure to add the trace to.
    trace : Union[BaseTraceType, dict]
        The trace to add.
    row : int, optional, default=1
        The row of the subplot.
    col : int, optional, default=1
        The column of the subplot.
    yaxis : int, optional, default=1
        The index of the y-axis.

    Returns
    -------
    go.Figure
        The figure with the added trace.
    """
    if yaxis > 1:
        trace.yaxis = f"y{get_yaxis_id(fig, row, col, yaxis)}"
        trace.xaxis = f"x{get_yaxis_id(fig, row, col, 1)}"
        return fig.add_trace(trace)
    else:
        return fig.add_trace(trace, row=row, col=col)


def update_traces(fig: go.Figure, row: int = 1, col: int = 1, yaxis: int = 1, **kwargs) -> go.Figure:
    """
    Updates the traces of the subplot at the given row and column belonging to the given y-axis. If yaxis == 1, the traces of the primary y-axis are updated, and equals
    the update_traces(...) method of plotly.graph_objs.Figure. If yaxis > 1, the traces of the secondary y-axis are updated.

    Parameters
    ----------
    fig : go.Figure
        The figure to update.
    row : int, optional, default=1
        The row of the subplot.
    col : int, optional, default=1
        The column of the subplot.
    yaxis : int, optional, default=1
        The index of the y-axis.
    **kwargs
        The arguments passed to the update_traces(...) method of plotly.graph_objs.Figure. I.e., the traces are updated with the given arguments.

    Returns
    -------
    go.Figure
        The figure with the updated traces.
    """
    if yaxis > 1:
        if "selector" in kwargs:
            selector = kwargs.pop("selector")
            selector = dict(yaxis=f"y{get_yaxis_id(fig, row, col, yaxis)}", **selector)
        else:
            selector = dict(yaxis=f"y{get_yaxis_id(fig, row, col, yaxis)}")

        return fig.update_traces(selector=selector, **kwargs)
    else:
        return fig.update_traces(row=row, col=col, **kwargs)


def update_dict(d: dict, update: dict):
    """Recursively updates the dictionary d with the values from the dictionary update."""
    for k, v in update.items():
        if isinstance(v, dict):
            d[k] = update_dict(d.get(k, {}), v)
        else:
            d[k] = v
    return d
