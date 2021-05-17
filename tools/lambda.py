import json
import os
import requests
import boto3
import pymysql
import sys

api_url_base = 'https://api.up.com.au/api/v1/'
api_token = os.environ.get('api_token')
headers = {'Authorization': 'Bearer {}'.format(api_token)}

endpoint  = os.environ.get('endpoint')
username = os.environ.get('username')
password = os.environ.get('password')
database_name = os.environ.get('database_name')


# ********************************
# ** STANDARD RUNTIME FUNCTIONS **
# ********************************

def list_accounts():
    api_url = api_url_base + 'accounts'
    response = requests.get(api_url, headers=headers)
    accountDict = {}

    if response.status_code == 200:
        accountList = response.json().get('data')
        for account in accountList:
            accountDict.update({account.get('id') : account.get('attributes').get('displayName')})
    return accountDict

def create_list(api_url):
    if filterVar:
        response = requests.get(api_url, headers=headers, params={"filterVar" : "date"})
    elif not filterVar:
        response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        data = []
        data.append(response.json().get('data'))
        if response.json().get('links').get('next'):
            token = response.json().get('links').get('next')
            while token:
                response = requests.get(token, headers=headers)
                data.append(response.json().get('data'))
                token = response.json().get('links').get('next')
                if token:
                    print("Processing token: {}".format(token))
                else:
                    print("Finished processing tokens")
        return data
    else:
        print(response.status_code)

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

def retrieve_transaction_history():
    pass

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
