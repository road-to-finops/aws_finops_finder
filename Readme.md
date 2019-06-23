# aws_cloudtrail_finder

## Getting Started

These instructions will get you a copy of the Tool up and running on your local machine.
 - Clone Repo
 - Run the following commands

 ```

aws-vault exec <cred>
./multi_account.py -m <methods>

If you wish to run for just one account use:
./multi_account.py -m <methods> -a <account_id>

#### Methods
- stopped_ec2 - Stopped EC2
- cloudtrail - Extra cloud trails not org, audit or root (too change)
- eip - Unassigned eip
- elb - empty elb
- alb -empty alb

```

### Prerequisites

* Install Boto3
* Python3
* aws-vault

Access to the org IAM Role 'OrganizationAccountAccessRole'

Ref: https://boto3.readthedocs.io/en/latest/guide/quickstart.html



