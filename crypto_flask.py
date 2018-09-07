from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from charts import get_product_data, make_rate_plot
from forms import GetCryptoForm
from bokeh.embed import components

bootstrap = Bootstrap()
app = Flask(__name__)
app.secret_key = 'dev_key'
bootstrap.init_app(app)

# Index page
@app.route('/', methods=['GET', 'POST'])
def index(crypto='BTC', fiat='USD', gran=86400):
    form = GetCryptoForm()

    # This is not the optimal way to do it. I should really be using the 
    # form.validate_on_submit() method, but this is always failing for 
    # some reason. Maybe it's because I don't have any validators on the 
    # form. (But I thought forms were valid by default?) 
    if request.method == 'POST':
        crypto = form.crypto.data
        fiat = form.fiat.data
        gran = int(form.gran.data)

    product = crypto + '-' + fiat
    data = get_product_data(product=product, granularity=gran)
    fig = make_rate_plot(data)
    script, div = components(fig)

    return render_template('index.html', script=script, div=div, form=form)

# With debug=True, Flask server will auto-reload 
# when there are code changes
if __name__ == '__main__':
	app.run(port=5000, debug=True)

