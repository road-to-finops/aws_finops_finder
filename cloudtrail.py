import boto3
import pdb 
#


def extra_cloudtrail(account_id, client):
    cloudtrails = client.describe_trails( includeShadowTrails=True)
    trail_count = len(cloudtrails['trailList'])
    
    for trails in cloudtrails['trailList']:

        if trails['IsOrganizationTrail'] is False:
 
            other = trails['Name']
            s3 = trails['S3BucketName']
            event = trails['HasCustomEventSelectors']
            #print('%s,%s,%s,%s,%s,%s' %(team, account_id,other,s3, event, trail_count))

            result = {
                    "AccountId" : account_id,
                    "Name" : other,
                    "Bucket" : s3,
                    "Event" : event
                    }
            print(result)
    return result



if __name__ == "__main__":
    client = boto3.client('cloudtrail')
    extra_cloudtrail(None, client)
