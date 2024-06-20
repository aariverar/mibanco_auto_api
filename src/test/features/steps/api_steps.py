import requests
from behave import given, when, then
from src.test.library.excel_reader import data
import json
import urllib3

def get_data():
        return data("test_data.xlsx","Hoja1")

@given('se lee el endpoint y lo headers del excel "{datos}"')
def step_given_api_endpoint(context,datos):
    context.ejecutar =get_data()[int(datos)-1]["Ejecucion"]
    context.custom_message ="-"
    if context.ejecutar=="SI":
        #Ignorar advertencia (solo para desarrolllo/pruebas)
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        context.endpoint = get_data()[int(datos)-1]["Endpoint"]
        if get_data()[int(datos)-1]["Headers"]:
            context.headers = dict([header.split(': ') for header in (get_data()[int(datos)-1]["Headers"]).split('\n')])
        else:
            context.headers=''
        if get_data()[int(datos)-1]["Params"]:
            context.params = dict([Params.split(': ') for Params in (get_data()[int(datos)-1]["Params"]).split('\n')])
        else:
            context.params=''
        context.request_type = get_data()[int(datos)-1]["Request Type"]
        context.expected_status_code = get_data()[int(datos)-1]["Expected Status Code"]
        context.expected_content = get_data()[int(datos)-1]["Expected Content_1"]
        context.custom_message = f"Se extrae: \nEndpoint: {context.endpoint}"
        print("[LOG] Se extrae del excel los datos")

@when('cuando envio un request al endpoint "{datos}"')
def step_when_send_request(context, datos):
    try:
        context.custom_message ="-"
        if context.ejecutar=="SI":
            print("[LOG] Se envia la peticion")
            if context.request_type == 'GET': 
                context.response = requests.get(context.endpoint, headers=context.headers,params=context.params,verify=False)
            elif context.request_type == 'POST':

                if get_data()[int(datos)-1]["Body"]:
                    context.body = json.loads(get_data()[int(datos)-1]["Body"])
                    context.response = requests.post(context.endpoint, headers=context.headers,params=context.params,json=context.body,verify=False)
                else:
                    context.body = ''
                    context.response = requests.post(context.endpoint, headers=context.headers,params=context.params,verify=False)
            elif context.request_type == 'PUT':
                context.response = requests.put(context.endpoint, headers=context.headers,params=context.params,verify=False)
            else:
                raise ValueError(f"Unsupported request type: {context.request_type}")
            log_messages = "<strong>REQUEST:</strong>\n"
            log_messages += f"{context.request_type} {context.response.url}\n"
            log_messages += f"Request Headers: {pretty_print_headers(context.response.request.headers)}\n"
            if get_data()[int(datos)-1]["Body"]:
                    log_messages += f"Body: {pretty_print_headers(context.body)}"
            if get_data()[int(datos)-1]["Params"]:
                log_messages += f"Params: {pretty_print_headers(context.params)}\n"
            log_messages += "\n\n<strong>RESPONSE:</strong>\n"
            log_messages += f"{context.response.request.method} - Code: {context.response.status_code} {context.response.reason}\n"
            log_messages += f"Headers: {pretty_print_headers(context.response.headers)}\n"
            log_messages += f"Elapsed Time: {context.response.elapsed}\n"
            log_messages += f"{pretty_print_headers(context.response.json())}\n"
            context.custom_message = log_messages
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
            log_messages = ""
            log_messages += "[LOG] Se valida el status Code\n"
            log_messages += f"Expected Status Code: {context.expected_status_code}\n"
            log_messages += f"Actual Status Code: {context.response.status_code}\n"
            context.custom_message = log_messages
            assert str(context.response.status_code) == str(context.expected_status_code)
        else:
            context.state="NO-EXECUTED"
            context.custom_message = "NO-EXECUTED"
    except Exception as e:
            print("[LOG] Error al validar el estado del response")
            log_messages += f"\nError al validar el estado del response:{e}"
            context.custom_message = log_messages
            raise AssertionError("[LOG] Error al validar el estado del response")
    
@then('el response debe contener el contenido esperado del excel "{datos}"')
def step_then_response_contains_expected_content(context,datos):
    try:
        context.custom_message ="HOLA"
        if context.ejecutar=="SI":
            validacion=" "
            print("[LOG] Se valida el contenido del response")
            log_messages = ""
            log_messages += "\n[LOG] Se valida el contenido del response\n\n"
            print(f"Actual Content: {pretty_print_headers(context.response.json())}")
            log_messages += f"<strong>Actual Content:</strong> {pretty_print_headers(context.response.json())}\n\n\n" 
            for i in range(1, 7, 1):
                vString=f"Expected Content_{i}"
                print(vString)
                if get_data()[int(datos)-1][vString]:
                    context.expected_content= get_data()[int(datos)-1][vString]
                    print(f"Expected Content: {context.expected_content}")
                    log_messages += f"Expected Content {i}: {context.expected_content}\n"
                    if context.expected_content in pretty_print_headers(context.response.json()):
                        log_messages+="<strong>PASSED</strong>\n\n"
                        validacion+="PASSED "
                    else:
                        log_messages+="<strong>FAILED</strong>\n\n"
                        validacion+="FAILED "
                else:
                    break    
            if validacion != " ":
                 print(validacion)
                 assert "FAILED" not in validacion
                 print("[LOG] Se realizo la validación del contenido correctamente!")
            else:
                 log_messages="No hay validaciones"                
            
            context.custom_message = log_messages
        else:
            context.state="NO-EXECUTED"
            context.custom_message = "NO-EXECUTED"
    except Exception as e:
            context.custom_message =f"Error al validar el contenido del response:{log_messages}{e}"
            print("[LOG] Error al validar el contenido del response")
            raise AssertionError("[LOG] Error al validar el contenido del response")



def convert_headers_to_dict(headers):
    return {key: value for key, value in headers.items()}

# Función para mostrar los encabezados en formato pretty
def pretty_print_headers(headers):
    # Convertir a un diccionario estándar si es un CaseInsensitiveDict
    if isinstance(headers, requests.structures.CaseInsensitiveDict):
        headers = convert_headers_to_dict(headers)
    pretty_headers = json.dumps(headers, indent=4)
    return pretty_headers