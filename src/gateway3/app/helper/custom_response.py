
from flask import Response, json


class CustomResponse(Response):
    def __init__(self, succeeded=True, message="", data=None, status=200, **kwargs):
        # Prepare the response data
        response_data = {
            "succeeded": succeeded,
            "message": message,
            "data": data if data is not None else {}
        }

        # Ensure the response is in JSON format
        response_json = json.dumps(response_data)

        # Additional headers can be added via kwargs if necessary
        headers = kwargs.get('headers', {})

        # Ensure the content type is set to application/json
        headers['Content-Type'] = 'application/json'

        super(CustomResponse, self).__init__(
            response=response_json, status=status, headers=headers)
