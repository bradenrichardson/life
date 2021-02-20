import boto3
import argparse

parser = argparse.ArgumentParser(description="Deploy cloudformation stacks to AWS")
parser.add_argument('--stack_name', type=str, required=True)
parser.add_argument('--create', type=bool)
parser.add_argument('--delete', type=bool)
args = parser.parse_args()

cf_client = boto3.client('cloudformation')

def create_stack():
    cf_template = open('infra.yml').read()
    cf_client.create_stack(StackName=args.stack_name, TemplateBody=cf_template, Capabilities=[
        'CAPABILITY_IAM',  'CAPABILITY_NAMED_IAM'])

def delete_stack():
    cf_client.delete_stack(StackName=args.stack_name)

if __name__ == '__main__':
    if args.create:
        create_stack()
    if args.delete:
        delete_stack()