import json
import os
import requests
import boto3

# API variables
api_url_base = 'https://api.up.com.au/api/v1/'
api_token = os.environ.get('api_token')
headers = {'Authorization': 'Bearer {}'.format(api_token)}

# S3 variables

def retrieve_transaction(transaction_id):
    api_url = api_url_base + 'transactions/' + transaction_id 
    response = requests.get(api_url, headers=headers)
    data = response.json()
    dictionary = {
        'ID' : transaction_id,
        'Description' : data.get('data').get('attributes').get('description'),
        'Value' : data.get('data').get('attributes').get('amount').get('value')[1:],
        'Created At' : data.get('data').get('attributes').get('createdAt')
    }
    if data.get('data').get('attributes').get('amount').get('value') < 0:
        pass
    if data.get('data').get('relationships').get('category').get('data'):
        dictionary['Category'] = data.get('data').get('relationships').get('category').get('data').get('id')
    else:
        dictionary['Category'] = 'Uncategorized'
    if data.get('data').get('relationships').get('parentCategory').get('data'):
        dictionary['Parent Category'] = data.get('data').get('relationships').get('parentCategory').get('data').get('id')
    else:
        dictionary['Parent Category'] = 'Uncategorized'
    return dictionary

def write_to_s3(transaction):
    pass

def lambda_handler(event, context):
    transaction_id = event.get('data').get('relationships').get('transaction').get('data').get('id')
    transaction = retrieve_transaction(transaction_id)
    write_to_s3(transaction)
