#!/usr/bin/env python3

import aws_cdk as cdk

from ecb_europa_currency_exchange_tracking_app.ecb_europa_currency_exchange_tracking_app_stack import EcbEuropaCurrencyExchangeTrackingAppStack


app = cdk.App()
EcbEuropaCurrencyExchangeTrackingAppStack(app, "ecb-europa-currency-exchange-tracking-app")

app.synth()
