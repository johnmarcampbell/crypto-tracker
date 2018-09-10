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
            choices=[('86400', '1 day'),
                    ('21600', '6 hours'),
                    ('3600', '1 hour'),
                    ('900', '15 minutes'),
                    ('300', '5 minutes'),
                    ('60','1 minute')
                    ])

    submit = SubmitField('Get Rates')

class GetStockForm(FlaskForm):
    stock = StringField('Ticker Symbol:', validators=[DataRequired()])
    submit = SubmitField('Get Rates')
