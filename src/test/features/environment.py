# features/environment.py
import time
import pandas as pd
import json
import os
from src.test.library.utils import modify_json_with_message
from src.test.library.reporte_html import generate_html_report
from datetime import datetime

def before_all(context):
    context.step_messages = []
    context.start_time=datetime.now()
    
    # Formatear la fecha y hora según el formato especificado
    formato = "%d %b %Y, %H:%M"
    context.fecha_formateada = context.start_time.strftime(formato)
    

def after_all(context):
    rutaJson= os.getcwd()+"\\json.pretty.output"
    with open(rutaJson, "a") as json_file:
        json_file.write("]") 
    
    with open(rutaJson, 'r') as file:
        data = json.load(file)
    # Modificar los nombres de los steps en el JSON
    modified_data = modify_json_with_message(data, context.step_messages)
    # Sobrescribir el archivo JSON con los cambios
    rutaJson2= os.getcwd()+"\\Nuevo.pretty.output"
    with open(rutaJson2, 'w') as file:
        json.dump(modified_data, file, indent=4)

    rutaJson= os.getcwd()+"\\Nuevo.pretty.output"

# Load the test results JSON
    with open(rutaJson, 'r') as file:
        test_results = json.load(file)

    
    # Generate the HTML report
    rutareporte=os.getcwd()+"\\src\\test\\reports\\test_report2.html"
    context.timer=datetime.now()-context.start_time
    context.fecha_formateada+=f" - Duracion: {context.timer.total_seconds()}s"
    generate_html_report(test_results, rutareporte,context.fecha_formateada)

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
    
