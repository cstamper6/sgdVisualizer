import random
import math
from sympy import *
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
import numpy as np

y = np.array([[0., 1., 2., 3., 4., 5., 6., 7., 8., 9.],
              [0., 1., 2., 3., 4., 5., 6., 7., 8., 9.],
              [0., 1., 2., 3., 4., 5., 6., 7., 8., 9.],
              [0., 1., 2., 3., 4., 5., 6., 7., 8., 9.],
              [0., 1., 2., 3., 4., 5., 6., 7., 8., 9.],
              [0., 1., 2., 3., 4., 5., 6., 7., 8., 9.],
              [0., 1., 2., 3., 4., 5., 6., 7., 8., 9.],
              [0., 1., 2., 3., 4., 5., 6., 7., 8., 9.],
              [0., 1., 2., 3., 4., 5., 6., 7., 8., 9.],
              [0., 1., 2., 3., 4., 5., 6., 7., 8., 9.]])

x = np.transpose(y)
z = np.zeros((10, 10))

app = dash.Dash(__name__)

axis = {
    "showbackground": True,
    "backgroundcolor": "black",
    "gridcolor": "white",
    "zerolinecolor": "white"
}

plotLayout = {
    "showlegend": False,
    "font": {
        "color": "white"
    },
    "plot_bgcolor": "black",
    "paper_bgcolor": "black",
    "scene": {
        "xaxis": axis,
        "yaxis": axis,
        "zaxis": axis,
        "camera": {
            "eye": {
                "x": "1.5",
                "y": "-2",
                "z": "0.5"
            }
        }
    },
    "height": "580"
}


app.layout = html.Div(
    [
        html.Div(
            [
                html.Div(dcc.Graph(
                    id='my-graph',
                    figure={
                        'data': [
                            go.Surface(z=z),
                            go.Scatter3d(
                                x=[0, 8],
                                y=[0, 8],
                                z=[0, 8],
                                marker=dict(
                                    colorscale='Jet'
                                )
                            )
                        ],
                        "layout": plotLayout
                    }
                ),
                )
            ],
            style={
                "float": "left",
                "width": "55%",
                "height": "580px",
                "margin": "25px",
                "border-radius": "10px",
                "border": "10px solid black"
            }
        ),
        # Function input box
        html.Div(
            [
                html.Div(dcc.Input(
                    id='input-box',
                    placeholder='Enter a value...',
                    type='text',
                    value='x**y',
                    style={"border": "4px solid red"}
                )),
                html.Button('Submit', id='button')
            ],
            style={
                "overflow": "hidden",
                "height": "580px",
                "margin": "25px",
                "margin-left": "0px",
                "border-radius": "10px",
                "border": "10px solid black",
                "background-color": "black"
            }
        )
    ],
    style={
        # "opacity": "0.8",
        "background-color": "lightgrey",
        "position": "fixed",
        "width": "100%",
        "height": "100%",
        "top": "0px",
        "left": "0px",
        "z-index": "1000",
    }
)


@app.callback(
    dash.dependencies.Output('my-graph', 'figure'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('input-box', 'value')])
def update_function(n_clicks, value):
    return {
        'data': [
            go.Surface(z=eval(value)),
            go.Scatter3d(
                
                # replace with return value of get points

                x=[0, 4, 8],
                y=[0, 4, 8],
                z=[0, 75, 150],
                marker=dict(
                    size=4,
                    colorscale='Jet'
                ),
                line=dict(
                    color='white',
                    width=10
                )
            )
        ],
        'layout': plotLayout
    }


if __name__ == '__main__':
    app.run_server(debug=True)

# Start of Math
x, y, z = symbols('x y z')
init_printing(use_unicode=True)

# The following function takes in the x, y, and
# stepsize values as INTEGERS and the equation as a function
# of x and y as a STRING.

# The data in the coords list is going to be of the form
#[a, b, c, d, e, f, d, e, f, g, h, i, g, h, i, j, k, l, ...]

coords = []

def getPoints(x_value, y_value, equation, step_size):

    equation_plugin = eval(equation)
    f = lambdify((x, y), equation_plugin)
    z_start = f(x_value, y_value)

    z_values = np.zeros(360)
    for i in range(360):
        x_grad = x_value + 0.0001*math.cos((i*math.pi)/180)
        y_grad = y_value + 0.0001*math.sin((i*math.pi)/180)
        z_values[i] = f(x_grad, y_grad)

    thetadegrees_approx = np.argmin(z_values)
    lowtheta = thetadegrees_approx - 1

    z_valueprecisemin = np.zeros(201)
    for i in range(201):
        x_gradprecise = x_value + 0.0001 * \
            math.cos((((i/100)+lowtheta)*math.pi)/180)
        y_gradprecise = y_value + 0.0001 * \
            math.sin((((i/100)+lowtheta)*math.pi)/180)
        z_valueprecisemin[i] = f(x_gradprecise, y_gradprecise)

    thetahundredths = np.argmin(z_valueprecisemin)
    theta_precise = lowtheta + thetahundredths/100

    z_start = f(x_value, y_value)
    x_dest = x_value + step_size*math.cos((theta_precise*math.pi)/180)
    y_dest = y_value + step_size*math.sin((theta_precise*math.pi)/180)

    z_end = f(x_dest, y_dest)

    coords.append(x_value)
    coords.append(y_value)
    coords.append(z_start)
    coords.append(x_dest)
    coords.append(y_dest)
    coords.append(z_end)

    if (z_start > z_end and x_dest < 10 and x_dest > -10 and y_dest < 10 and y_dest > -10):
        getPoints(x_dest, y_dest, equation, step_size)
    else:
        return coords
        # turn into scatter 3d line


truecoords = []
for i in range(len(coords)):
    if (i/3) % 2 != 1:
        truecoords.append(coords[i])

getPoints(9, 9, "x**2 + y**2", 2)
print(truecoords)
