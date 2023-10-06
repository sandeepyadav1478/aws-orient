# Usages
SERVICE_NAME = "execute-api"
ENDPOINT = "https://3kphode371.execute-api.ap-south-1.amazonaws.com/asd/pets/?k1=v1"
payload = {"ds":"sd"}  # Your JSON payload


from botocore.awsrequest import AWSRequest
import requests
import json
import logging
from typing import Any
from clients.aws_client import AWSClient


class AWSApiGatewayClient:
    def __init__(self, aws_client: AWSClient, service_name: str) -> None:
        if not isinstance(aws_client, AWSClient):
            raise ValueError("aws_client must be an instance of AWSClient")
        self.aws_client = aws_client
        self.service_name = service_name

    def get(self, endpoint: str) -> requests.Response:
        try:
            request = AWSRequest(method='GET', url=endpoint)
            self.aws_client.sign_request(request, self.service_name)
            response = requests.get(request.url, headers=request.headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            logging.error("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            logging.error("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            logging.error("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            logging.error("Something went wrong with the request", err)
        return response

    def post(self, endpoint: str, payload: Any) -> requests.Response:
        headers = {'Content-Type': 'application/json'}
        try:
            request = AWSRequest(method='POST', url=endpoint, data=json.dumps(payload), headers=headers)
            self.aws_client.sign_request(request, self.service_name)
            response = requests.post(request.url, data=request.body, headers=request.headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            logging.error("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            logging.error("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            logging.error("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            logging.error("Something went wrong with the request", err)
        return response


aws_client = AWSClient()
api_gateway_client = AWSApiGatewayClient(aws_client, SERVICE_NAME)

# Send a GET request
get_response = api_gateway_client.get(ENDPOINT)
print(get_response.content)

# Send a POST request with a JSON payload
post_response = api_gateway_client.post(ENDPOINT, payload)
print(post_response.content)

# Clearing out cache
aws_client.clear_cache()