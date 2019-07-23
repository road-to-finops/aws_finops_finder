import time
import pandas as pd
import xlsxwriter
import boto3
import json
from lambda_base import generate_csv
from flatten_dict import flatten

# Use the temporary credentials that AssumeRole returns to make a
# connection to Amazon IAM


def append_data(check_name, team_info, resource, meta_result):
    temp = {}
    temp.update(check_name)
    temp.update(team_info)
    temp.update(resource)
    temp.update(meta_result)
    return temp


def get_checks(account_id, client):
    result = []
    response = client.describe_trusted_advisor_checks(language="en")

    for case in response["checks"]:
        team_info = {"account_id": account_id}
        meta = case["metadata"]
        if case["category"] == "cost_optimizing":
            c_id = case["id"]
            check_name = {"name": case["name"], "id": c_id}

            check_result = client.describe_trusted_advisor_check_result(
                checkId=c_id, language="en"
            )

            if check_result["result"]["status"] == "warning":
                flaggedResources = {
                    "flaggedResources": check_result["result"]["flaggedResources"]
                }

                for resource in flaggedResources.get("flaggedResources"):
                    meta_result = dict(zip(meta, resource["metadata"]))
                    updated = append_data(check_name, team_info, resource, meta_result)
                    result.append(updated)
    return result
    """
    print(json.dumps(result))
   
    attach_file = generate_csv(result, headings=['name', 'id', 'resourceId', 'team', 'account_id', 'region', 'status', 'Estimated Monthly Savings', 'Monthly Storage Cost','Estimated Monthly Savings (On Demand)'])
    print(attach_file)
    """


if __name__ == "__main__":

    client = boto3.client("support", region_name="us-east-1")
    get_checks(None, client)
