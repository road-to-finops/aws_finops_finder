import boto3
from botocore.exceptions import ClientError
import pdb


def classic_elb(account, client):
    elb_list = []

    lbs = client.describe_load_balancers()

    for classic_elb in lbs['LoadBalancerDescriptions']:
        elb_name = classic_elb['LoadBalancerName']
        instance_health = client.describe_instance_health(
            LoadBalancerName=elb_name
        )
        if instance_health['InstanceStates'] == []:
            #print('%s is empty' %elb_name)
            elb_list.append(alb_arn)
    result = {
        "AccountId" : account,
        "alb" : elb_list
    }
    print(result)




def app_elb(account, client):

    alb_list = []
    lbs = client.describe_load_balancers()
    for application_elb in lbs['LoadBalancers']:
        alb_arn = application_elb['LoadBalancerArn']
        
        target_groups = client.describe_target_groups(
        LoadBalancerArn=alb_arn
        )
        for targetgroup in target_groups['TargetGroups']:
            targetgroup_arn = targetgroup['TargetGroupArn']

            response = client.describe_target_health(
            TargetGroupArn=targetgroup_arn,
            )
            if response['TargetHealthDescriptions'] == []:  
                #print('%s is empty' %alb_arn)
                alb_list.append(alb_arn)
    result = {
        "AccountId" : account,
        "alb" : alb_list
    }
    print(result)
    '''
    else:
        for TargetHealthDescriptions in response['TargetHealthDescriptions']:
            TargetHealth = TargetHealthDescriptions['TargetHealth']
            if TargetHealth['State'] == 'unhealthy':
                print('%s is unhealth' %alb_arn)
    '''



       


if __name__ == "__main__":
    client = boto3.client('elb')
    elb(None, client)
