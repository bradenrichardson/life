import requests
import json
import csv
import argparse

## TODO: Create list_balance function


parser = argparse.ArgumentParser(description="A tool to export UP transactions in a CSV file")
parser.add_argument('--api_token', type=str)
parser.add_argument('--create_csv', type=bool)
parser.add_argument('--since', type=str)
parser.add_argument('--until', type=str)
parser.add_argument('--create_webhook', type=bool)
parser.add_argument('--ping_webhook', type=bool)
parser.add_argument('--list_webhooks', type=bool)
parser.add_argument('--retrieve_webhook', type=bool)
parser.add_argument('--delete_webhook', type=bool)
parser.add_argument('--list_webhook_logs', type=bool)
parser.add_argument('--retrieve_transaction', type=bool)
parser.add_argument('--sample_request', type=bool)
parser.add_argument('--create_list', type=bool)
args = parser.parse_args()

api_url_base = 'https://api.up.com.au/api/v1/'
headers = {'Authorization': 'Bearer {}'.format(args.api_token)}

if args.since:
    filterVar = 'filter[since]'
    date = args.since + 'T00:00:00+10:00'

if args.until:
    filterVar = 'filter[until]'
    date = args.until + 'T00:00:00+10:00'

if not args.until and not args.since:
    filterVar = False



# def list_balance():
#     api_url = api_url_base + 'accounts'
#     response requests.get(api_url, headers=headers)
# up:yeah:vps3uC0otXFRO9PQ6jtq1ZylzQSdwQikBDX2tWcUmK4vl0LdZaZ0S9pd9IOnOVuTVD4EYpNQELJQHcuOD51kqFNUNgniFh3QN4UXSKN3m9EHJ7IpyLonYKzsSjReCAoK

def sample_request():
    response = requests.get('https://linuxacademy.com')
    print(response)

def create_webhook():
    api_url = api_url_base + 'webhooks' 
    data_object = {"data": {"attributes": {"url" : "https://mc8w4cnc83.execute-api.ap-southeast-2.amazonaws.com/Default/UpWebhook"}}}
    print(data_object)
    response = requests.post(api_url, headers=headers, json=data_object)
    print(response.text)

def retrieve_webhook():
    api_url = api_url_base + 'webhooks' + '/ff1fa884-792a-4924-8f64-788d4b4eabaf'
    response = requests.get(api_url, headers=headers)
    print(response.text)

def list_webhooks():
    api_url = api_url_base + 'webhooks'
    response = requests.get(api_url, headers=headers)
    print(response.text)

def delete_webhook():
    api_url = api_url_base + 'webhooks' + '/ff1fa884-792a-4924-8f64-788d4b4eabaf'
    response = requests.delete(api_url, headers=headers)
    print(response)

def ping_webhook():
    api_url = api_url_base + 'webhooks' + '/ff1fa884-792a-4924-8f64-788d4b4eabaf' + '/ping'
    response = requests.post(api_url, headers=headers, json={'key':'value','key':'value','key':'value'})
    print(response.text)

def list_webhook_logs():
    api_url = api_url_base + 'webhooks' + '/ff1fa884-792a-4924-8f64-788d4b4eabaf'  + '/logs'
    response = requests.get(api_url, headers=headers)
    with open ('logfile.txt', 'w') as logfile:
        for i in response:
            logfile.write(str(i))
            logfile.write('\n')

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
    
    

def create_csv():
    api_url = api_url_base + 'transactions'
    accounts = list_accounts()
    data = create_list(api_url)
    csvDictionary = {'id' : [], 'description' : [], 'value' : [], 'category' : [], 'parentCategory' : [], 'createdAt' : [], 'account' : []}


    for array in data:
        for transaction in array:
            # Rewrite this
            # Probably check if there is information about whether it's going to a saver or not
            if 'Transfer' in transaction.get('attributes').get('description'):
                continue
            if 'transfer' in transaction.get('attributes').get('description'):
                continue
            if 'Cover' in transaction.get('attributes').get('description'):
                continue
            if 'Round Up' in transaction.get('attributes').get('description'):
                continue
            else:
                csvDictionary['id'].append(transaction.get('id'))
                csvDictionary['description'].append(transaction.get('attributes').get('description'))
                csvDictionary['value'].append(transaction.get('attributes').get('amount').get('value'))
                if transaction.get('relationships').get('category').get('data'):
                    csvDictionary['category'].append(transaction.get('relationships').get('category').get('data').get('id'))
                else:
                    csvDictionary['category'].append('Uncategorized')
                if transaction.get('relationships').get('parentCategory').get('data'):
                    csvDictionary['parentCategory'].append(transaction.get('relationships').get('parentCategory').get('data').get('id'))
                else:
                    csvDictionary['parentCategory'].append('Uncategorized')
                csvDictionary['createdAt'].append(transaction.get('attributes').get('createdAt'))
                csvDictionary['account'].append(accounts.get(transaction.get('relationships').get('account').get('data').get('id')))

    try:
        with open("csv_file.csv", 'w', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter = ",")
            writer.writerow(csvDictionary.keys())
            writer.writerows(zip(*csvDictionary.values()))
    except IOError:
        print("I/O error")
        
def retrieve_transaction():
    api_url = api_url_base + 'transactions' + '/2eed0d66-8a2d-4569-a0c1-975096c38506'
    response = requests.get('https://linuxacademy.com')
    print(response)

     # transaction_id = event.get('data').get('relationships').get('transaction').get('data').get('id')
if __name__ == '__main__':
    print("Verifying API access token")
    api_url = api_url_base + 'transactions'
    if args.create_csv:
        create_csv()
    if args.create_webhook:
        create_webhook()
    if args.ping_webhook:
        ping_webhook()
    if args.list_webhooks:
        list_webhooks()
    if args.retrieve_webhook:
        retrieve_webhook()
    if args.delete_webhook:
        delete_webhook()
    if args.list_webhook_logs:
        list_webhook_logs()
    if args.retrieve_transaction:
        retrieve_transaction()
    if args.sample_request:
        sample_request()
    if args.create_list:
        create_list(api_url)
    