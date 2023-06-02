## Deployment Instructions

The steps mentioned below are for deployment on AWS.

Install [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

Install AWS CDK
```bash
$ npm install -g aws-cdk
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
Install Python packages required to run the app
```bash
$ pip install -r requirements.txt
```
Run the following command to bootstrap the deployment
```bash
$ cdk bootstrap
```

(Optional) Run this command if you want to generate CloudFormation Template
```bash
$ cdk synth
```

Run the following command to deploy application on AWS
```bash
$ cdk deploy
```

Once the application has been deployed. It will give you an endpoint on the app is currently running. Copy that endpoint and append **exchange-rate-info** to access the API endpoint.

Run the following command to delete the application and removing allocated resources
```bash
$ cdk destroy
```
