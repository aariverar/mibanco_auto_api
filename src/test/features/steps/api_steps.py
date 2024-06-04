import requests
from behave import given, when, then

@given('the API endpoint is read from the Excel file')
def step_given_api_endpoint(context):
    print(f"Endpoint: {context.endpoint}")

@given('the headers are read from the Excel file')
def step_given_headers(context):
    print(f"Headers: {context.headers}")

@when('I send a "{request_type}" request to the endpoint')
def step_when_send_request(context, request_type):
    context.request_type = request_type
    if request_type == 'GET':
        context.response = requests.get(context.endpoint, headers=context.headers)
    elif request_type == 'POST':
        context.response = requests.post(context.endpoint, headers=context.headers)
    elif request_type == 'PUT':
        context.response = requests.put(context.endpoint, headers=context.headers)
    else:
        raise ValueError(f"Unsupported request type: {request_type}")

@then('the response status code should be read from the Excel file')
def step_then_response_status_code(context):
    print(f"Expected Status Code: {context.expected_status_code}")
    print(f"Actual Status Code: {context.response.status_code}")
    assert context.response.status_code == context.expected_status_code

@then('the response should contain the expected content from the Excel file')
def step_then_response_contains_expected_content(context):
    print(f"Expected Content: {context.expected_content}")
    print(f"Actual Content: {context.response.text}")
    assert context.expected_content in context.response.text
