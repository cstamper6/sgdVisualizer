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
app.layout = html.Div(
    [
        html.Div(dcc.Graph(
            id='my-graph',
            figure={
                'data': [
                    go.Surface(z=z)
                ]
            })),
        html.Div(dcc.Input(
            id='input-box',
            placeholder='Enter a value...',
            type='text',
            value='-1/(x**2+y**2)'
        )),
        html.Button('Submit', id='button')
    ]
)


@app.callback(
    dash.dependencies.Output('my-graph', 'figure'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('input-box', 'value')])
def update_function(n_clicks, value):
    return {'data': [go.Surface(z=eval(value))]}


if __name__ == '__main__':
    app.run_server(debug=True)
