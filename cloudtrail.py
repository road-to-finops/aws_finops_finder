import boto3
import pdb 
#


def extra_cloudtrail(team, account_id, client):
    cloudtrails = client.describe_trails( includeShadowTrails=True)
    trail_count = len(cloudtrails['trailList'])
    
    for trails in cloudtrails['trailList']:
        if trails['IsOrganizationTrail'] is False and trails['Name'] != 'RootTrail' and 'audit' not in trails['Name']:

            other = trails['Name']
            s3 = trails['S3BucketName']
            event = trails['HasCustomEventSelectors']
            print('%s,%s,%s,%s,%s,%s' %(team, account_id,other,s3, event, trail_count))
    


if __name__ == "__main__":
    client = boto3.client('cloudtrail')
    extra_cloudtrail(None, client)
