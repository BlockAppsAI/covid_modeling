import datetime


colors = {
    'background': '#e5ecf6',
    'text': '#194278',
    'lines': '#f93b2e',
}

xaxis = dict(
    rangeselector=dict(
        buttons=[
            dict(count=1,
                 label="1m",
                 step="month",
                 stepmode="backward"),
            dict(count=3,
                 label="3m",
                 step="month",
                 stepmode="backward"),
            dict(count=6,
                 label="6m",
                 step="month",
                 stepmode="backward"),
            dict(count=1,
                 label="YTD",
                 step="year",
                 stepmode="todate"),
            dict(count=1,
                 label="1y",
                 step="year",
                 stepmode="backward"),
            dict(step="all")
        ]
    ),
    rangeslider=dict(
        visible=True,
    ),
    type="date",
    autorange=False,
    showgrid=False,
    range=[datetime.datetime.now().date() - datetime.timedelta(days=30), datetime.datetime.now().date()]
)

yaxis = {
    'anchor': 'x',
    'autorange': True,
    'rangemode': 'tozero',
    'showline': True,
    'tickmode': 'auto',
    'rangemode': 'tozero',
    'showgrid': False,
}

plot_margins = dict(
    l=5, r=5, b=5, t=5, pad=5
)

figure_params = {
    # 'title_font_family': 'Arial Black',
    'xaxis': xaxis,
    'yaxis': yaxis,
    'title_x': 0.5,
    # 'font_color': colors['text'],
    'margin': plot_margins,
    # 'plot_bgcolor': 'rgba(229, 236, 246, 1.0)',
}

scatter_style = {
    'mode': 'markers+lines+text',
    'marker': {
        # 'color': colors['lines'],
        'size': 8,
    },
    'line': {
        "width": 2.0,
        # "color": colors['lines']
    },
    'showlegend': True,
}

rt_scatter_style = {
    'mode': 'lines+text',
    'marker': {
        # 'color': colors['lines'],
        'size': 8,
    },
    'line': {
        "width": 2.0,
        # "color": colors['lines']
    },
    'showlegend': True,
}

empty_data_dict = {
    "layout": {
        "xaxis": {
            "visible": False
        },
        "yaxis": {
            "visible": False
        },
        "annotations": [
            {
                "text": "No matching data found",
                "xref": "paper",
                "yref": "paper",
                "showarrow": False,
                "font": {
                    "size": 28
                }
            }
        ]
    }
}