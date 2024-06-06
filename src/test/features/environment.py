# features/environment.py
import time
import pandas as pd
import json
import os
from src.test.library.utils import modify_json_with_message

def before_all(context):
    """
    Hook to execute before all tests.
    Use this to set up global context attributes, configurations, etc.
    """
    context.step_messages = []

def after_all(context):
    """
    Hook to execute after all tests.
    Use this to clean up any resources initialized in before_all.
    """
    print(context.step_messages)
    rutaJson= os.getcwd()+"\\json.pretty.output"
    with open(rutaJson, "a") as json_file:
        json_file.write("]") 
    
    print(rutaJson)
    with open(rutaJson, 'r') as file:
        data = json.load(file)
    # Modificar los nombres de los steps en el JSON
    modified_data = modify_json_with_message(data, context.step_messages)
    # Sobrescribir el archivo JSON con los cambios
    rutaJson2= os.getcwd()+"\\Nuevo.pretty.output"
    with open(rutaJson2, 'w') as file:
        json.dump(modified_data, file, indent=4)
    print("PAUSA")
    

def before_feature(context, feature):
    """
    Hook to execute before each feature.
    """


def after_feature(context, feature):
    """
    Hook to execute after each feature.
    """


def before_scenario(context, scenario):
    context.state=None

def after_scenario(context, scenario):
    if context.state is not None:
        scenario.set_status("skipped")
    # You can add cleanup code here if necessary

def before_step(context, step):
    """
    Hook to execute before each step.
    """

def after_step(context, step):
    if context.ejecutar=="NO":
        context.custom_message = "NO-EXECUTED"

    if hasattr(context, 'custom_message'):
        step_message = {
            'step_name': step.name,
            'message': context.custom_message
        }
        context.step_messages.append(step_message)

    
    if step.status == "failed":
        # You can add code here to handle step failures
        print(f"Step failed: {step.name}")
    
