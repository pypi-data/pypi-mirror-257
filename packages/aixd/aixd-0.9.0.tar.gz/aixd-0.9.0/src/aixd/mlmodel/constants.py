# Constants folder

import plotly.express as px

RANDOM_SEED_SPLIT = 22  # To enforce always the same splits
SEP_LOSSES = "/"  # With / we enforce in Wandb different folders

# color mappings
pastel = px.colors.qualitative.Pastel
t10 = px.colors.qualitative.T10
colors = {
    "data": {"train": pastel[0], "val": pastel[1], "test": pastel[2]},
    "latent": {"single": px.colors.sequential.YlGnBu, "mu": {"main": "steelblue", "sec": "dodgerblue"}, "std": {"main": "seagreen", "sec": "limegreen"}},
    "attr": {"y": "papayawhip", "y_hat": "lightgreen", "y_rec_hat": "yellowgreen"},
    "attr_err": {"y_hat": "coral", "y_rec_hat": "orangered"},
    "x_err": {"main": t10[0], "sec": "lightskyblue"},
    "y_err": {"main": t10[1], "sec": "sandybrown"},
    "de": {"main": t10[2], "sec": "lightsalmon"},
    "de_s": {"main": t10[3], "sec": "paleturquoise"},
    "uncertainty": "steelblue",
}
