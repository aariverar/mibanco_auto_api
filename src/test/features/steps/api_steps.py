import requests
from behave import given, when, then
from src.test.library.excel_reader import data
import json

def get_data():
        return data("test_data.xlsx","Hoja1")

@given('se lee el endpoint y lo headers del excel "{datos}"')
def step_given_api_endpoint(context,datos):
    context.ejecutar =get_data()[int(datos)-1]["Ejecucion"]
    context.custom_message ="-"
    if context.ejecutar=="SI":
        context.endpoint = get_data()[int(datos)-1]["Endpoint"]
        if get_data()[int(datos)-1]["Headers"]:
            context.headers = dict([header.split(': ') for header in (get_data()[int(datos)-1]["Headers"]).split('\n')])
        else:
            context.headers=''
        context.request_type = get_data()[int(datos)-1]["Request Type"]
        context.expected_status_code = get_data()[int(datos)-1]["Expected Status Code"]
        context.expected_content = get_data()[int(datos)-1]["Expected Content"]
        context.custom_message = f"Se extrae: \nEndpoint: {context.endpoint}"
        print("[LOG] Se extrae del excel los datos")

@when('cuando envio un request al endpoint "{datos}"')
def step_when_send_request(context, datos):
    try:
        context.custom_message ="-"
        if context.ejecutar=="SI":
            print("[LOG] Se envia la peticion")
            if context.request_type == 'GET':
                
                context.response = requests.get(context.endpoint, headers=context.headers)
                
            elif context.request_type == 'POST':

                if get_data()[int(datos)-1]["Body"]:
                    context.body = json.loads(get_data()[int(datos)-1]["Body"])
                    context.response = requests.post(context.endpoint, headers=context.headers,json=context.body)
                else:
                    print("VACIO")
                    context.body = ''
                    context.response = requests.post(context.endpoint, headers=context.headers)
                

            elif context.request_type == 'PUT':
                context.response = requests.put(context.endpoint, headers=context.headers)
            else:
                raise ValueError(f"Unsupported request type: {context.request_type}")
            print(f"Response: {context.response.json()}")
            context.custom_message = f"Response: {context.response.json()}"
            
    except Exception as e:
            print("[LOG] Error realizar la peticion:",e)
            context.custom_message =f"Error realizar la peticion:{e}"
            raise AssertionError("[LOG] Error al validar el contenido del response")


@then('se valida el estado del response con el esperado del excel "{datos}"')
def step_then_response_status_code(context,datos):
    try:
        context.custom_message ="HOLA"
        if context.ejecutar=="SI":
            print("[LOG] Se valida el status Code")
            print(f"Expected Status Code: {context.expected_status_code}")
            print(f"Actual Status Code: {context.response.status_code}")
            assert str(context.response.status_code) == str(context.expected_status_code)
            log_messages = ""
            log_messages += "[LOG] Se valida el status Code\n"
            log_messages += f"Expected Status Code: {context.expected_status_code}\n"
            log_messages += f"Actual Status Code: {context.response.status_code}\n"
            context.custom_message = log_messages
        else:
            context.state="NO-EXECUTED"
            context.custom_message = "NO-EXECUTED"
    except Exception as e:
            print("[LOG] Error al validar el estado del response")
            context.custom_message =f"Error al validar el estado del response:{e}"
            raise AssertionError("[LOG] Error al validar el estado del response")
    
@then('the response should contain the expected content from the Excel file "{datos}"')
def step_then_response_contains_expected_content(context,datos):
    try:
        context.custom_message ="HOLA"
        if context.ejecutar=="SI":
            print("[LOG] Se valida el contenido del response")
            print(f"Expected Content: {context.expected_content}")
            print(f"Actual Content: {context.response.text}")
            log_messages = ""
            log_messages += "[LOG] Se valida el contenido del response\n"
            log_messages += f"Expected Content: {context.expected_content}\n"
            log_messages += f"Actual Content: {context.response.text}\n"
            assert context.expected_content in context.response.text
            
            print("[LOG] Se realizo la validación del contenido correctamente!")
            context.custom_message = log_messages
        else:
            context.state="NO-EXECUTED"
            context.custom_message = "NO-EXECUTED"
    except Exception as e:
            context.custom_message =f"Error al validar el contenido del response:{log_messages}{e}"
            print("[LOG] Error al validar el contenido del response")
            raise AssertionError("[LOG] Error al validar el contenido del response")
