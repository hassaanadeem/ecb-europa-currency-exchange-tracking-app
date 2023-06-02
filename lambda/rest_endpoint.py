import os
import json

import boto3

TABLE_NAME = os.environ["TABLE_NAME"]

LOCALSTACK_ENPOINT = None
if "LOCALSTACK_HOSTNAME" in os.environ:
    LOCALSTACK_ENPOINT = f'http://{os.environ["LOCALSTACK_HOSTNAME"]}:4566'


def handler(event, context):
    data_from_db = get_data_from_database()
    response = api_response_builder(data_from_db)
    return response


# READS DATA FROM DYNAMODB
def get_data_from_database():
    dynamodb = boto3.resource("dynamodb", endpoint_url=LOCALSTACK_ENPOINT)
    table = dynamodb.Table(TABLE_NAME)
    response = table.scan()
    items = response["Items"]

    while "LastEvaluatedKey" in response:
        response = table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
        items.extend(response["Items"])

    return items


# PREPARES THE API RESPONSE
def api_response_builder(data_objects):
    response = {
        "publish_date": "N/A",
        "base_currency": "EUR",
        "rates_info": list(),
    }

    for db_doc in data_objects:
        if db_doc["id"] == "publish_date":
            response["publish_date"] = db_doc["value"]
        else:
            response_item = {
                "currency": db_doc["id"],
                "rate": db_doc["rate"],
                "change_in_rate": db_doc["change"],
                "change_percentage": db_doc["change_percent"],
            }
            response["rates_info"].append(response_item)

    response["rates_info"] = sorted(response["rates_info"], key=lambda x: x["currency"])
    return {"statusCode": 200, "body": json.dumps(response, indent=4)}
