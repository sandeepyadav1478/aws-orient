#!/usr/bin/env python3

from json import load
from pathlib import Path
from boto3 import client

class DeletePolicy:
    """
    Can delete any policy
    for any account
    """

    def __init__(self) -> None:
        self.service_name = "iam"
        # file which holds credentials
        with open(Path().cwd() / 'credentials.json', 'r') as f:
            self.creds = load(f)
    
    def issueClient(self, account: dict) -> object:
        """
        Set aws account on
        boto3 client
        """
        # Create a Boto3 IAM client for the specified AWS account
        self.client = client(self.service_name, aws_access_key_id=account.get("aws_access_key_id",None), aws_secret_access_key=account.get("aws_secret_access_key",None), aws_session_token=account.get("aws_session_token",""))
    
    def DeletePolicies(self):
        """
        method does the
        """
        for acc_policy in self.creds:
            try:
                # issue a client
                self.issueClient(acc_policy)
                # Delete the IAM policy
                self.client.delete_policy(PolicyArn=f'arn:aws:iam::{acc_policy.get("aws_acount_id",None)}:policy/{acc_policy.get("aws_policy_name",None)}')
            except Exception as e:
                print(f'Some error occured for policy {acc_policy.get("aws_policy_name",None)} in account {acc_policy.get("aws_acount_id",None)}: {e}')
            else:
                print(f'Successfully deleted policy {acc_policy.get("aws_policy_name",None)} in account {acc_policy.get("aws_acount_id",None)}')
    
if __name__ == "__main__":
    obj = DeletePolicy()
    obj.DeletePolicies()