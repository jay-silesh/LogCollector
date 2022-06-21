import json

import requests

from src.entities.response import Response
from src.exceptions.client_error import ClientError, ClientErrorCode


def send_get_request(api_url) -> (int, dict):
    try:
        response = requests.get(api_url)
        json_response = json.loads(response.text)
        return response.status_code, json_response
    except requests.ConnectionError as e:
        return get_http_response_code(e), {}
    except Exception as e:
        return get_http_response_code(e), {}


def get_http_response_code(resp) -> int:
    if isinstance(resp, Response):
        if not resp.logs:
            return 204  # No Content
        if resp.is_offset:
            return 206  # Partial content
        return 200

    if isinstance(resp, ClientError):
        if resp.code == ClientErrorCode.FILE_NOT_FOUND:
            return 404
        # Send ClientErrorCode.BAD_REQUEST by default
        return 400

    if isinstance(resp, NotImplementedError):
        return 501

    if isinstance(resp, ConnectionError):
        return 503

    # ServerError
    return 500
