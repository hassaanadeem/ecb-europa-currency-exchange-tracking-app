
# Serverless Currency Exchange Tracking Application

This is an exchange rates tracking application. This application uses the data provided by [European Central Bank](https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html) fetched periodically and stored in the database. This application also evaluates each currency's performance against the previous day's price. The application exposes a public REST API endpoint to fetch the data. This applications is deployable on AWS and LocalStack using the AWS CDK.  

The application uses the following AWS Services.
1. AWS Lambda
2. AWS DynamoDB
3. AWS API Gateway

## Deployment Instructions

The steps mentioned below are for deployment on Localstack. If you want to deploy on AWS, follow this guide. 

Install AWS CDK
```bash
$ npm install -g aws-cdk-local aws-cdk
```
Clone the repository
```bash
$ git clone git@github.com:hassaanadeem/ecb-europa-currency-exchange-tracking-app.git
```
Create Python virtual environment
```bash
$ python3 -m venv .venv
```
Activate the virtual enviroment
```bash
// For linux and mac
$ source .venv/bin/activate

// Windows
$ .\venv\Scripts\activate
```
Install *awslocal*
```bash
$ pip install awscli-local
```
Run the following command to install Python packages
```bash
$ pip install -r requirements.txt
```
Create an account on LocalStack [here](https://app.localstack.cloud/sign-in) and opt for free trial. Also grab your API-KEY from your account

Install [Localstack](https://docs.localstack.cloud/getting-started/installation/).

Run the following commands to start the LocalStack
```bash
$ export LOCALSTACK_API_KEY=<YOUR_API_KEY>
$ localstack start
```
Run the following command to bootstrap the deployment
```bash
$ cdklocal bootstrap
```

(Optional) Run this command if you want to generate CloudFormation Template
```bash
$ cdklocal synth
```

Run the following command to deploy application on Localstack
```bash
$ cdklocal deploy
```

Once the application has been deployed. It will give you an endpoint on the app is currently running. Copy that endpoint and append **exchange-rate-info** to access the API endpoint.

Run the following command to stop the localstack
```bash
$ localstack stop
```
## Running tests

Run the following command to install dev dependencies
```bash
$ pip install -r requirements-dev.txt
```
Run the following command to run tests
```bash
$ python3 -m pytest -v
```
