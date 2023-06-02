import os
import boto3
import urllib.error
import urllib.request
import xml.etree.ElementTree as xml_et


TABLE_NAME = os.environ["TABLE_NAME"]
SOURCE_URL = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-90d.xml"
XML_NS = "{http://www.ecb.int/vocabulary/2002-08-01/eurofxref}Cube"

LOCALSTACK_ENPOINT = None
if "LOCALSTACK_HOSTNAME" in os.environ:
    LOCALSTACK_ENPOINT = f'http://{os.environ["LOCALSTACK_HOSTNAME"]}:4566'


def handler(event, context):
    response_data = extract(SOURCE_URL)

    current_date, transformed_data = transform(response_data)

    load(current_date, transformed_data)


def extract(endpoint):
    response = urllib.request.urlopen(endpoint, timeout=30)

    return response


def transform(response_data):
    exchange_data = response_data.read()

    raw_data = read_xml(exchange_data)
    current_day, data_transformed = currency_performance(raw_data)

    return current_day, data_transformed


def load(date, daily_exchange_data):
    dynamodb = boto3.resource("dynamodb", endpoint_url=LOCALSTACK_ENPOINT)
    table = dynamodb.Table(TABLE_NAME)

    with table.batch_writer() as writer:
        writer.put_item(Item={"id": "publish_date", "value": date})
        for currency, data in daily_exchange_data.items():
            data["id"] = currency
            writer.put_item(Item=data)


def read_xml(xml):
    xml_root = xml_et.fromstring(xml)
    xml_root = xml_root.find(XML_NS)

    days_counter = 0
    daily_data = dict()
    for x in xml_root.iter():
        if not bool(x.attrib):
            continue

        if "time" in x.attrib.keys():
            date = x.attrib.get("time")
            days_counter += 1
            if days_counter == 3:
                break
            daily_data[date] = {}
            continue

        if "currency" in x.attrib.keys() and "rate" in x.attrib.keys():
            currency = x.attrib.get("currency")
            rate = x.attrib.get("rate")
            daily_data[date].update({currency: rate})
    return daily_data


def currency_performance(data):
    current_day, previous_day = data.keys()

    previous_data = data[previous_day]
    current_data = data[current_day]

    exchange_rates_data = {}

    for currency, rate in current_data.items():
        if currency not in previous_data:
            continue

        previous_rate = float(previous_data[currency])
        current_rate = float(rate)

        rate_change = round(current_rate - previous_rate, 4)

        rate_change_percentage = round((rate_change / previous_rate) * 100, 4)

        exchange_rates_data[currency] = {
            "rate": f"{current_rate}",
            "change": f"{rate_change}",
            "change_percent": f"{rate_change_percentage}%",
        }

    return current_day, exchange_rates_data
