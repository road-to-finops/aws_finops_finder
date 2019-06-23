# aws_cloudtrail_finder

# Elatic IP Realse
Find any unassociated EIPs and gives the option to release them

## Getting Started

These instructions will get you a copy of the Tool up and running on your local machine.

### Prerequisites

* Install Boto3
* Python3
* aws-vault

Access to the org IAM Role 'OrganizationAccountAccessRole'

Ref: https://boto3.readthedocs.io/en/latest/guide/quickstart.html


### Running the Tool

Clone the Tool and run as below

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
A Prompt will ask you if you wish to realse the ip use yes and no


**********************

aws-vault exec <role>
./multi_account.py 