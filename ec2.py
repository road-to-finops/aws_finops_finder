import boto3
from botocore.exceptions import ClientError


def stopped_ec2(account, client):
    # create filter for instances in running state

    filters = [
        {
            'Name': 'instance-state-name', 
            'Values': ['stopped']
        }
    ]
    
    # filter the instances based on filters() above
    response = client.describe_instances(Filters=filters)

    instancelist = []
    for reservation in (response["Reservations"]):
        for instance in reservation["Instances"]:
            instancelist.append(instance["InstanceId"])
    
    result = {
        "AccountId" : account,
        "instance" : instancelist
    }
    return result

    
if __name__ == "__main__":
    client = boto3.client('ec2')
    stopped_ec2(None, client)