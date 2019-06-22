#!/usr/bin/env python3
import logging
import boto3
from botocore.exceptions import ClientError
from tqdm import tqdm
import argparse
import boto3
import pdb

import org
import eip
import ec2
import elb
import cloudtrail
log = logging.getLogger()


class BaseManager:
    def __init__(self, session, region):
        self.session = session
        self.region = region

    @property
    def client(self):
        if not hasattr(self, "_client"):
            self._client = self.session.client(self._name, region_name=self.region)
        return self._client

    @property
    def resource(self):
        if not hasattr(self, "_resource"):
            self._resource = self.session.resource(self._name, region_name=self.region)
        return self._resource


class RechargerManager(BaseManager):
    _name = "dynamodb"

    def __init__(self, session, region, recharger_table):
        super().__init__(session, region)
        self.recharger_table = recharger_table

    def get_dynamodb_table(self, table_name):
        if not hasattr(self, f"_{table_name}"):
            log.info(f"Getting table: {table_name}")
            table = self.resource.Table(table_name)
            setattr(self, f"_{table_name}", [item for item in table.scan()["Items"]])
        return getattr(self, f"_{table_name}")

    def get_service_teams(self):
        recharger = self.get_dynamodb_table(self.recharger_table)
        return {row["service_team"]["name"] for row in recharger}

    def get_team_accounts(self, team, exceptions):
        # Get a dictionary of account names/nums relating to service team
        accounts = []
        for row in self.get_dynamodb_table(self.recharger_table):
            if row["service_team"]["name"] == team:
                for acc in row.get("service_accounts", []):
                    if (
                        acc.get("account_name") not in exceptions["account_names"]
                        or acc.get("account_id") not in exceptions["account_ids"]
                    ):
                        accounts.append(acc)

        return accounts

def configure_parser():
    parser = argparse.ArgumentParser(description="Identify idle/unused EBS volumes")
    parser.add_argument('-m', required=True, choices=['eip', 'stopped_ec2', 'elb', 'alb', 'cloudtrail'], help='which function do you want to use')
    args = parser.parse_args()

    #global method
    method = args.m
    return method



def assume_role_recharger( role_session_name):
    role_arn = 'arn:aws:iam::165293267760:role/RootAccountAdmin'
    log.info(f"Trying to Assume Role with arn: {role_arn}")
    try:
        sts_client = boto3.client("sts")
        assumed_role_object = sts_client.assume_role(
            RoleArn=role_arn, RoleSessionName=role_session_name
        )
        creds = assumed_role_object["Credentials"]
        boto_session = boto3.session.Session(
            creds["AccessKeyId"], creds["SecretAccessKey"], creds["SessionToken"]
        )

        return boto_session
    except ClientError as e:
        if e.response["Error"]["Code"] == "AccessDenied":
            log.error(f"Unable to Assume Role with arn: {role_arn}")
        raise


def get_unmanaged():
    # waiting for recharger functionality for unmanaged accounts
    return {
        "account_names": [
            "IAM-Dev",
            "KPMG D&A AWS 2",
            "KPMG D&A AWS 1",
            "KPMG D&A AWS 3",
        ],
        "account_ids": [""],
    }


def assume_role(account_id, service):
    
    role_arn = "arn:aws:iam::%s:role/OrganizationAccountAccessRole" % account_id
    sts_client = boto3.client('sts')
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
        )
        return client

    except ClientError as e:
        #print("Unexpected error Account %s: %s" % (account_id, e))
        return None
   



def main():
    method = configure_parser() 
   '''
    session = assume_role_recharger("patch_report")
    recharger = RechargerManager(session, 'eu-west-1', "recharger.services")
    accounts = {}

    for team in tqdm(recharger.get_service_teams()):
        team_accounts = recharger.get_team_accounts(team, get_unmanaged())
        if team != "Unknown":
            #print(team)


    for account in team_accounts:
        account_id = account['account_id']
    '''
    team_accounts  = org.list_accounts
    for account_id in team_accounts:
        try:
            if len(account_id) < 15:
                if method == 'eip':
                    client = assume_role(account_id, 'ec2')
                    print(eip.free_elastic_ip(account_id, client))
                elif method == 'stopped_ec2':
                    client = assume_role(account_id, 'ec2')
                    stopped  = ec2.stopped_ec2(account_id, client)
                    #s_list.append(stopped)
                    print(stopped)
                elif method == 'elb':
                    client = assume_role(account_id, 'elb')
                    elb_code  = elb.classic_elb(account_id, client)
                elif method == 'alb':
                    client = assume_role(account_id, 'elbv2')
                    alb  = elb.app_elb(account_id, client)
                elif method == 'cloudtrail':
                    client = assume_role(account_id, 'cloudtrail')
                    cloudtrail_result  = cloudtrail.extra_cloudtrail(team, account_id, client)
                    
            
        except Exception as e:
            pass
            #print(e)


if __name__ == "__main__":
    main()