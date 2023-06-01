import aws_cdk as core
import aws_cdk.assertions as assertions
from ecb_europa_currency_exchange_tracking_app.ecb_europa_currency_exchange_tracking_app_stack import EcbEuropaCurrencyExchangeTrackingAppStack


def test_sqs_queue_created():
    app = core.App()
    stack = EcbEuropaCurrencyExchangeTrackingAppStack(app, "ecb-europa-currency-exchange-tracking-app")
    template = assertions.Template.from_stack(stack)

    template.has_resource_properties("AWS::SQS::Queue", {
        "VisibilityTimeout": 300
    })


def test_sns_topic_created():
    app = core.App()
    stack = EcbEuropaCurrencyExchangeTrackingAppStack(app, "ecb-europa-currency-exchange-tracking-app")
    template = assertions.Template.from_stack(stack)

    template.resource_count_is("AWS::SNS::Topic", 1)
