from sklearn.manifold import TSNE
import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors, AllChem
import seaborn as sns
from rdkit.Chem.rdFingerprintGenerator import FingeprintGenerator64
from rdkit.Chem import rdFingerprintGenerator

import plotly.graph_objects as go
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, no_update, callback


data_path = 'database/ox2r_pos_tsne.csv'
df_all = pd.read_csv(data_path)

patent_names = df_all["专利名称"].unique()
color_sequence = px.colors.qualitative.Alphabet[:30]

# 创建一个字典，将每个专利名称映射到一个特定的颜色
color_map = {patent_name: color_sequence[i % len(color_sequence)] for i, patent_name in enumerate(patent_names)}

# 将"专利名称"列映射到颜色
df_all['color'] = df_all['专利名称'].map(color_map)

fig = go.Figure(data=[
    go.Scatter(
        x=df_all["t-SNE1"],
        y=df_all["t-SNE2"],
        mode="markers",
        marker=dict(
            color=df_all["color"],           # 使用映射的颜色
            size=df_all["MW"],               # 大小根据 MW 列设置
            line={"color": "#444"},
            sizeref=45,
            sizemode="diameter",
            opacity=0.8,
        )
    )
])
fig.update_traces(hoverinfo="none", hovertemplate=None)

fig.update_layout(
    xaxis=dict(title='t-SNE1'),
    yaxis=dict(title='t-SNE2'),
    plot_bgcolor='rgba(255,255,255,0.1)'
)

app = Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id="graph-basic-2", figure=fig, clear_on_unhover=True),
    dcc.Tooltip(id="graph-tooltip"),
])


@callback(
    Output("graph-tooltip", "show"),
    Output("graph-tooltip", "bbox"),
    Output("graph-tooltip", "children"),
    Input("graph-basic-2", "hoverData"),
)

def display_hover(hoverData):
    if hoverData is None:
        return False, no_update, no_update

    # demo only shows the first point, but other points may also be available
    pt = hoverData["points"][0]
    bbox = pt["bbox"]
    num = pt["pointNumber"]

    df_row = df_all.iloc[num]
    img_src = df_row['url']
    name = df_row['公司名称']
    form = df_row['Value']
    desc = df_row['SMILES']
    if len(desc) > 300:
        desc = desc[:100] + '...'

    children = [
        html.Div([
            html.Img(src=img_src, style={"width": "100%"}),
            html.H2(f"{name}", style={"color": "darkblue", "overflow-wrap": "break-word"}),
            html.P(f"{form}"),
            html.P(f"{desc}"),
        ], style={'width': '200px', 'white-space': 'normal'})
    ]
    return True, bbox, children

if __name__ = "__main__":
	app.run(debug=True)