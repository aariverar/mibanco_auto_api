# utils.py
import json
import io
from functools import wraps

def modify_json_with_message(json_data,step_messages):
    for feature in json_data:
        for element in feature.get('elements', []):
            for step in element.get('steps', []):
                # Buscar el mensaje correspondiente para este step
                for msg in step_messages:
                    if msg['step_name'] == step['name']:
                        # Añadir el mensaje personalizado al step
                        print(msg['step_name'])
                        print(msg['message'])
                        step['result']['message'] = msg['message']
                        break
    return json_data
