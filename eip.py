import boto3
from botocore.exceptions import ClientError


def free_elastic_ip(account, client):

        response = client.describe_addresses()
        #for each ip check if it is associated, if it is move on
        elastic_ip = [address["PublicIp"] for address in response['Addresses'] if address.get("AssociationId") is None]

        result = {
            "AccountId" : account,
            "IpAddresses" : elastic_ip
        }
        return result

if __name__ == "__main__":
    client = boto3.client('ec2')
    free_elastic_ip(None, client)