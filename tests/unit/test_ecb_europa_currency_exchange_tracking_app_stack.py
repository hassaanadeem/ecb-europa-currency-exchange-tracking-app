import aws_cdk as core
import aws_cdk.assertions as assertions
from ecb_europa_currency_exchange_tracking_app.ecb_europa_currency_exchange_tracking_app_stack import (
    EcbEuropaCurrencyExchangeTrackingAppStack,
)


def test_dynamodb_table_created():
    app = core.App()
    stack = EcbEuropaCurrencyExchangeTrackingAppStack(
        app, "ecb-europa-currency-exchange-tracking-app"
    )
    template = assertions.Template.from_stack(stack)
    template.has_resource_properties(
        "AWS::DynamoDB::Table",
        {
            "KeySchema": [{"AttributeName": "id", "KeyType": "HASH"}],
            "AttributeDefinitions": [{"AttributeName": "id", "AttributeType": "S"}],
        },
    )
    template.has_resource("AWS::DynamoDB::Table", {"DeletionPolicy": "Delete"})


def test_etl_routine_lambda_created():
    app = core.App()
    stack = EcbEuropaCurrencyExchangeTrackingAppStack(
        app, "ecb-europa-currency-exchange-tracking-app"
    )
    template = assertions.Template.from_stack(stack)
    template.has_resource_properties(
        "AWS::Lambda::Function",
        {
            "Handler": "etl_routine.handler",
            "Runtime": "python3.9",
            "Timeout": 240,
            "Environment": {"Variables": {"TABLE_NAME": {}}},
        },
    )


def test_rest_endpoint_lambda_created():
    app = core.App()
    stack = EcbEuropaCurrencyExchangeTrackingAppStack(
        app, "ecb-europa-currency-exchange-tracking-app"
    )
    template = assertions.Template.from_stack(stack)
    template.has_resource_properties(
        "AWS::Lambda::Function",
        {
            "Handler": "rest_endpoint.handler",
            "Runtime": "python3.9",
            "Timeout": 60,
            "Environment": {"Variables": {"TABLE_NAME": {}}},
        },
    )


def test_rest_api_gateway_created():
    app = core.App()
    stack = EcbEuropaCurrencyExchangeTrackingAppStack(
        app, "ecb-europa-currency-exchange-tracking-app"
    )
    template = assertions.Template.from_stack(stack)
    template.has_resource_properties(
        "AWS::ApiGateway::RestApi", {"Name": "rest-api-rates"}
    )
    template.has_resource_properties(
        "AWS::ApiGateway::Resource", {"PathPart": "exchange-rate-info"}
    )
    template.has_resource_properties("AWS::ApiGateway::Method", {"HttpMethod": "GET"})
