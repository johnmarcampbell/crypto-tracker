from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField

class GetDataForm(FlaskForm):
    crypto = SelectField('Cryptocurrency',
            choices=[('btc','BTC'),
                    ('eth', 'ETH'),
                    ('bch', 'BCH')
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
