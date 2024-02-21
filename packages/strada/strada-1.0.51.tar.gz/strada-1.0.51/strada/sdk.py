import requests
from .common import (
    hydrate_input_fields,
    validate_http_input,
    fill_path_params,
)
from .custom_types import StradaError, StradaHttpResponse 

class HttpRequestExecutor:
    @staticmethod
    def execute(
        dynamic_parameter_json_schema: dict,
        base_path_params,
        base_headers,
        base_query_params,
        base_body,
        base_url: str,
        method: str,
        header_overrides: dict = {},
        function_name: str = None,
        app_name: str = None,
        **kwargs
    ) -> StradaHttpResponse:
        validate_http_input(dynamic_parameter_json_schema, **kwargs)

        path_params = hydrate_input_fields(
            dynamic_parameter_json_schema, base_path_params, **kwargs
        )
        headers = hydrate_input_fields(
            dynamic_parameter_json_schema, base_headers, **kwargs
        )
        query_params = hydrate_input_fields(
            dynamic_parameter_json_schema, base_query_params, **kwargs
        )
        body = hydrate_input_fields(dynamic_parameter_json_schema, base_body, **kwargs)

        for key, value in header_overrides.items():
            headers[key] = value

        url = fill_path_params(base_url, path_params)
        
        if (
            headers.get("Content-Type") == "application/json"
            or headers.get("content-type") == "application/json"
        ):
            if method in ["get", "delete"]:
                response = requests.request(
                    method, url, headers=headers, params=query_params
                )
            else:
                response = requests.request(
                    method, url, headers=headers, params=query_params, json=body
                )
        else:
            if method in ["get", "delete"]:
                response = requests.request(
                    method, url, headers=headers, params=query_params
                )
            else:
                response = requests.request(
                    method, url, headers=headers, params=query_params, data=body
                )

        if response.ok:  # HTTP status code 200-299
            try:
                response_data = response.json()
                return StradaHttpResponse(
                    success=True, 
                    data=response_data,
                    error=None,
                    status_code=response.status_code,
                    headers=dict(response.headers),
                )
            except:
                return StradaHttpResponse(
                    success=True, 
                    data=response.text,
                    error=None,
                    status_code=response.status_code,   
                    headers=dict(response.headers),
                )
        else:
            response_data = None
            error_message = None
            if response.headers.get("Content-Type") == "application/json" or response.headers.get("content-type") == "application/json":
                response_data = response.json()

                # If the response contains structured error information, you can parse it here
                error_message = response_data.get("message", None)
                if error_message is None:
                    error_message = response_data.get("error", None)
                    if 'message' in error_message:
                        error_message = error_message['message']
                if error_message is None:
                    error_message = response.text
                if error_message is None:
                    error_message = "Error executing HTTP Request."
            else:
                error_message = response.text
                response_data = response.text

            error = StradaError(
                errorCode=response.status_code,
                statusCode=response.status_code,
                message=error_message,
            )
            
            response_model = StradaHttpResponse(
                success=False, 
                data=response_data, 
                error=error,
                status_code=response.status_code,
                headers=dict(response.headers),
            )
            
            return response_model
