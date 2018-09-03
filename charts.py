import cbpro
import pandas as pd
from bokeh.io import output_notebook, show
from bokeh.plotting import figure, ColumnDataSource
from bokeh.models import LinearAxis, Range1d, NumeralTickFormatter, HoverTool

def get_product_data(product='BTC-USD', granularity=86400):
    headings = ['time', 'low', 'high', 'open', 'close', 'volume']
    public_client = cbpro.PublicClient()
    data = public_client.get_product_historic_rates(product, granularity=granularity)
    data = pd.DataFrame(data, columns=headings)
    data['time'] = data['time'] * 1000. # Change microsenconds to milliseconds
    return data

def make_rate_plot(data, crypto_label='BTC', fiat_label='USD'):
    def axis_range(values, padding=0.1):
        delta = max(values) - min(values)
        low = min(values) - padding*delta
        high = max(values) + padding*delta
        return [low, high]

    title = crypto_label + ' Price'
    p = figure(x_axis_type="datetime", title=title, plot_height=350, plot_width=800)
    p.xgrid.grid_line_color=None
    p.ygrid.grid_line_alpha=0.5
    p.xaxis.axis_label = 'Time'
    
    # Make the hover tool-tip
    source = ColumnDataSource(data=data)
    hover = HoverTool()
    hover.tooltips = [('Open', '@open{($ 0,0.)}'),
                      ('Close', '@close{($ 0,0.)}'),
                      ('Low', '@low{($ 0,0.)}'),
                      ('High', '@high{($ 0,0.)}'),
                      ('Volume', '@volume{(0.00a)}')
                        ]
    p.add_tools(hover)

    # Set up the first y-axis
    p.yaxis.axis_label = 'Price (' + fiat_label + ')'
    p.y_range = Range1d(*axis_range(data['close']))
    p.yaxis.formatter = NumeralTickFormatter(format="$0,0.")
    p.line(x='time', y='close', line_width=2, source=source)
    
    # Set up the second y-axis
    p.extra_y_ranges = {'volumes': Range1d(start=0, end=axis_range(data['volume'])[1])}
    axis_right = LinearAxis(y_range_name='volumes', axis_label='Trade Volume (# of ' + crypto_label + ')', formatter=NumeralTickFormatter(format="0,0a"))
    p.add_layout(axis_right, 'right')
    p.rect(data['time'], data['volume']/2, width=1, height=data['volume'], y_range_name='volumes', color='grey', alpha=.4)

    p.toolbar.logo = None

    return p
