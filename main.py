#!/usr/bin/env python3
import logging
import boto3
from botocore.exceptions import ClientError
from tqdm import tqdm
import argparse
import boto3
import pdb

import eip
import ec2
import elb
import ebs
import cloudtrail
log = logging.getLogger()

def configure_parser():
    parser = argparse.ArgumentParser(description="Identify idle/unused EBS volumes")
    parser.add_argument('-m', required=True, choices=['eip', 'stopped_ec2', 'elb', 'alb', 'cloudtrail', 'ebs'], help='which function do you want to use')
    parser.add_argument('-a', required=False, help='Specific AWS Account you want to check')
    parser.add_argument('-region', help='which region you would like to look at', default=None)
    
    args = parser.parse_args()

    #global method
    method = args.m
    aws_account_id = args.a
    region = args.region
    return method, aws_account_id, region
 

def assume_role(account_id, service, region):
    
    role_arn = "arn:aws:iam::%s:role/OrganizationAccountAccessRole" % account_id
    sts_client = boto3.client('sts')

    if region is None:
        region = sts_client.meta.region_name
    try:

        assumedRoleObject = sts_client.assume_role(
            RoleArn=role_arn,
            RoleSessionName="AssumeRoleRoot"
            )
            
        credentials = assumedRoleObject['Credentials']
        client = boto3.client(
            service,
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken'],
            region_name = region
        )
        return client

    except ClientError as e:
        #print("Unexpected error Account %s: %s" % (account_id, e))
        return None
   

def list_accounts():
        client = boto3.client('organizations', region_name='us-east-1')
        paginator = client.get_paginator('list_accounts')
        response_iterator = paginator.paginate()
        account_ids = [account["Id"] for response in response_iterator for account in response["Accounts"] if account["Status"] != "SUSPENDED"]
        return account_ids


def main():
    method, aws_account_id, region = configure_parser() 
    if aws_account_id is not None:
        team_accounts = [aws_account_id]      
    else:
        team_accounts  = list_accounts()

    for account_id in tqdm(team_accounts):
        try:
            if len(account_id) < 15:
                if method == 'eip':
                    client = assume_role(account_id, 'ec2', region)
                    print(eip.free_elastic_ip(account_id, client))
                elif method == 'stopped_ec2':
                    client = assume_role(account_id, 'ec2', region)
                    stopped  = ec2.stopped_ec2(account_id, client)
                    #s_list.append(stopped)
                    print(stopped)
                elif method == 'elb':
                    client = assume_role(account_id, 'elb', region)
                    elb_code  = elb.classic_elb(account_id, client)
                elif method == 'alb':
                    client = assume_role(account_id, 'elbv2', region)
                    alb  = elb.app_elb(account_id, client)
                elif method == 'cloudtrail':
                    client = assume_role(account_id, 'cloudtrail', region)
                    cloudtrail_result  = cloudtrail.extra_cloudtrail(account_id, client)
                elif method == 'ebs':
                    client = assume_role(account_id, 'ec2', region)
                    ebs_result  = ebs.ebs(account_id, client)
            
            
        except Exception as e:
            pass
            print(e)


if __name__ == "__main__":
    main()