import boto3
from dotenv import load_dotenv
from botocore.awsrequest import AWSRequest
from botocore.auth import SigV4Auth
from os import getenv
from functools import lru_cache

# load variables into environment
load_dotenv(".awscreds")

class AWSClient:
    def __init__(self, region_name: str = getenv("REGION_NAME"), access_key: str = getenv("ACCESS_KEY"), secret_key: str = getenv("SECRET_KEY"), session_token: str = getenv("SESSION_TOKEN")) -> None:
        
        
        self.session = boto3.Session(region_name=region_name, aws_access_key_id=access_key, aws_secret_access_key=secret_key, aws_session_token=session_token)
        self.credentials = self.session.get_credentials().get_frozen_credentials()
        self.region_name = region_name

    @lru_cache(maxsize=None)
    def sign_request(self, request: AWSRequest, service_name: str) -> None:
        SigV4Auth(self.credentials, service_name, self.region_name).add_auth(request)
    
    def clear_cache(self):
        self.sign_request.cache_clear()