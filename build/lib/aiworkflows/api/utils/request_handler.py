import requests


def send_request(url, api_key, body: dict, method: str = 'POST', req_description: str = "sending request") -> dict:
    """
    Sends a request to the aiworkflows server.
    :param url:
    :param api_key:
    :param body:
    :param method:
    :param req_description:
    :return:
    """
    body['ApiKey'] = api_key

    response: requests.Response
    try:
        if method == 'POST':
            response = requests.post(url, json=body)
        elif method == 'GET':
            response = requests.get(url, json=body)
        else:
            raise ValueError(f'Error {req_description}: method {method} not supported.')
    except Exception as e:
        raise RuntimeError(f'Error {req_description}: {e}')

    if response.status_code != 200:
        raise RuntimeError(f'Error {req_description}: '
                           f'returned status code {response.status_code}, '
                           f'message: {response.text}')

    try:
        return response.json()
    except Exception as e:
        raise RuntimeError(f'Error {req_description}: parsing json failed for response: {e}')
