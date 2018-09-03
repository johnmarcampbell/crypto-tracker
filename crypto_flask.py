from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from charts import get_product_data, make_rate_plot
from bokeh.embed import components

bootstrap = Bootstrap()
app = Flask(__name__)
bootstrap.init_app(app)

# Index page
@app.route('/')
def index():
    data = get_product_data()
    fig = make_rate_plot(data)
    script, div = components(fig)
    return render_template('index.html', script=script, div=div)

# With debug=True, Flask server will auto-reload 
# when there are code changes
if __name__ == '__main__':
	app.run(port=5000, debug=True)

