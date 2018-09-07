import cbpro
import pandas as pd
from bokeh.plotting import figure, ColumnDataSource
from bokeh.models import LinearAxis, Range1d, NumeralTickFormatter, HoverTool

def get_product_data(product='BTC-USD', granularity=86400):
    ''' Retrieves price data for a given trading pair from Coinbase Pro API

    :product: A label for the trading pair to look up
    :granularity: A time interval (in seconds) to set the granularity of returned
    data. Must be one of [60, 300, 900, 3600, 21600, 86400]
    :rtype: pandas.DataFrame
    '''

    headings = ['time', 'low', 'high', 'open', 'close', 'volume']
    public_client = cbpro.PublicClient()
    data = public_client.get_product_historic_rates(product, granularity=granularity)
    data = pd.DataFrame(data, columns=headings)
    data['time'] = data['time'] * 1000. # Change microsenconds to milliseconds
    return data

def make_rate_plot(data, crypto_label='BTC', fiat_label='USD'):
    '''Makes a plot of cryptocurrency prices as a function of time
    
    :data: A pandas dataframe. Expected columns are ['time', 'open', 'close',
    'low', 'high', 'volume']
    :crypto_label: A label for the type of cryptocurrency being plotted. Typically
    a three letter abbreviation like BTC or ETH
    :fiat_label: A label for the type of fiat currency being plotted. Typically
    a three letter abbreviation like USD or EUR
    :rtype: bokeh.plotting.figure
    '''

    def axis_range(values, padding=0.1):
        ''' Determines axis ranges for a set of data, including some padding
        :values: The values that go in the plot
        :padding: The amount of padding above and below the data, expressed as a 
        fraction of the range (max - min) of the data.
        :rtype: list
        '''

        delta = max(values) - min(values)
        low = min(values) - padding*delta
        high = max(values) + padding*delta
        return [low, high]

    title = crypto_label + ' Price'
    p = figure(x_axis_type="datetime", title=title, plot_height=350, plot_width=800)
    p.toolbar.logo = None
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
    p.line(x='time', y='close', line_width=2, source=source,
            legend=crypto_label + ' Price')
    
    # Set up the second y-axis
    p.extra_y_ranges = {'volumes': Range1d(start=0, end=axis_range(data['volume'])[1])}
    axis_opts = {'y_range_name': 'volumes',
            'axis_label': 'Trade Volume (# of ' + crypto_label + ')',
            'formatter': NumeralTickFormatter(format="0,0a")
            }
    p.add_layout(LinearAxis(**axis_opts), 'right')

    rect_opts = {'width': 1,
            'height': data['volume'],
            'y_range_name': 'volumes',
            'color': 'grey',
            'alpha': .4,
            'legend': 'Trade Volume'
            }
    p.rect(data['time'], data['volume']/2, **rect_opts)

    return p
