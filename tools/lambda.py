import json
import os
import requests
import boto3
import pymysql
import sys

api_url_base = 'https://api.up.com.au/api/v1/'
api_token = os.environ.get('api_token')
headers = {'Authorization': 'Bearer {}'.format(api_token)}

endpoint  = os.environ.get('RDS_HOST')
username = os.environ.get('RDS_USERNAME')
password = os.environ.get('RDS_USER_PWD')
database_name = os.environ.get('RDS_DB_NAME')

ACCESS_KEY = os.environ.get('ACCESS_KEY')
SECRET_KEY = os.environ.get('SECRET_KEY')


# ********************************
# ** STANDARD RUNTIME FUNCTIONS **
# ********************************

def retrieve_transaction(transaction_id):
    api_url = api_url_base + 'transactions/' + transaction_id 
    response = requests.get(api_url, headers=headers)
    data = response.json()
    dictionary = {
        'ID' : transaction_id,
        'Description' : data.get('data').get('attributes').get('description'),
        'Value' : data.get('data').get('attributes').get('amount').get('value'),
        'Created At' : data.get('data').get('attributes').get('createdAt')
    }
    if data.get('data').get('relationships').get('category').get('data'):
        dictionary['Category'] = data.get('data').get('relationships').get('category').get('data').get('id')
    else:
        dictionary['Category'] = 'Uncategorized'
    if data.get('data').get('relationships').get('parentCategory').get('data'):
        dictionary['Parent Category'] = data.get('data').get('relationships').get('parentCategory').get('data').get('id')
    else:
        dictionary['Parent Category'] = 'Uncategorized'
    return dictionary

def update_database(transaction):
    try:
        connection = pymysql.connect(endpoint, user=username, passwd=password, db=database_name)
    except pymysql.MySQLError as e:
        print(e)
    print('establishing database connection')
    with connection.cursor() as cursor:
        cursor.execute('insert into Transactions (TransactionID, Description, Value, CreatedAt, ParentCategory, Category) values("{0}", "{1}", {2}, "{3}", "{4}", "{5}")'.format(transaction.get('ID'), transaction.get('Description'), transaction.get('Value'), transaction.get('Created At'), transaction.get('Parent Category'), transaction.get('Category')))
    connection.commit()

def lambda_handler(event, context):
    transaction_id = event.get('data').get('relationships').get('transaction').get('data').get('id')
    transaction = retrieve_transaction(transaction_id)
    update_database(transaction)
