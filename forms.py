from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired

class GetCryptoForm(FlaskForm):
    crypto = SelectField('Cryptocurrency',
            choices=[('BTC','BTC'),
                    ('ETH', 'ETH'),
                    ('BCH', 'BCH')
                    ])

    fiat = SelectField('Fiat currency',
            choices=[('usd','USD'),
                    ('eur', 'EUR'),
                    ])

    gran = SelectField('Time Slices',
            choices=[('60','1 minute'),
                    ('300', '5 minutes'),
                    ('900', '15 minutes'),
                    ('3600', '1 hour'),
                    ('21600', '6 hours'),
                    ('86400', '1 day'),
                    ])

    submit = SubmitField('Get Rates')

class GetStockForm(FlaskForm):
    stock = StringField('Ticker Symbol:', validators=[DataRequired()])
    submit = SubmitField('Get Rates')
