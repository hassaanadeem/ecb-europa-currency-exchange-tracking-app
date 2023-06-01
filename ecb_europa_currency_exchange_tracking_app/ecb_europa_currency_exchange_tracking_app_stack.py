from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_dynamodb,
    aws_lambda,
    aws_logs,
    aws_events,
    aws_events_targets,
    aws_apigateway,
    triggers,
    RemovalPolicy,
)

DYNAMO_DB_TABLE = "currency_exchange_rates"
DYNAMO_DB_TABLE_PARTITION_KEY = "id"

LAMBDA_FUNCTIONS_PATH = "./lambda"
LAMBDA_FUNCTION_RUN_HOUR_OF_THE_DAY = "20"


class EcbEuropaCurrencyExchangeTrackingAppStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # DYNAMODB TABLE
        dynamodb_table = aws_dynamodb.Table(
            self,
            DYNAMO_DB_TABLE,
            partition_key=dynamodb.Attribute(
                name=DYNAMO_DB_TABLE_PARTITION_KEY, type=dynamodb.AttributeType.STRING
            ),
            removal_policy=RemovalPolicy.DESTROY,
        )

        # LAMBDA FUNCTION 1: REST ENDPOINT
        lambda_rest_endpoint = aws_lambda.Function(
            self,
            "rest_endpoint",
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            timeout=Duration.seconds(60),
            code=aws_lambda.Code.from_asset(LAMBDA_FUNCTIONS_PATH),
            handler="rest_endpoint.handler",
            log_retention=aws_logs.RetentionDays.ONE_MONTH,
        )
        lambda_rest_endpoint.add_environment("TABLE_NAME", dynamodb_table.table_name)

        # LAMBDA FUNCTION 1: REST ENDPOINT
        lambda_etl_routine = aws_lambda.Function(
            self,
            "etl_routine",
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            timeout=Duration.minutes(4),
            code=aws_lambda.Code.from_asset(LAMBDA_FUNCTIONS_PATH),
            handler="etl_routine.handler",
            log_retention=aws_logs.RetentionDays.ONE_MONTH,
        )
        lambda_etl_routine.add_environment("TABLE_NAME", dynamodb_table.table_name)

        # DYNAMODB PERMISSIONS
        dynamodb_table.grant_read_write_data(lambda_etl_routine)
        dynamodb_table.grant_read_data(lambda_rest_endpoint)

        # APIGATEWAY: REST API ENDPOINT
        rest_api_endpoint = aws_apigateway.LambdaRestApi(
            self, "rest-api-rates", handler=lambda_rest_endpoint, proxy=False
        )
        rest_api_resource = rest_api_endpoint.root.add_resource("exchange-rate-info")
        rest_api_resource.add_method("GET")

        # EVENTS SCHEDULE: LAMBDA
        lambda_etl_routine_schedule = aws_events.Schedule.cron(
            hour=LAMBDA_FUNCTION_RUN_HOUR_OF_THE_DAY, minute="0"
        )
        lambda_etl_routine_target = aws_events_targets.LambdaFunction(
            handler=lambda_etl_routine
        )
        aws_events.Rule(
            self,
            "etl-routine-event",
            description="Daily trigger for exchange rates update lambda function",
            enabled=True,
            schedule=lambda_etl_routine_schedule,
            targets=[lambda_etl_routine_target],
        )

        # TRIGGER
        trigger = triggers.TriggerFunction(
            self,
            "init-etl-routine",
            execute_after=[dynamodb_table, lambda_etl_routine],
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            code=aws_lambda.Code.from_asset(LAMBDA_FUNCTIONS_PATH),
            handler="etl_routine.handler",
            execute_on_handler_change=False,
            timeout=Duration.minutes(4),
            log_retention=aws_logs.RetentionDays.ONE_MONTH,
        )
        trigger.add_environment("TABLE_NAME", dynamodb_table.table_name)

        # DYNAMODB PERMISSIONS
        dynamodb_table.grant_read_write_data(trigger)
