import json
import os
from datetime import datetime
from src.test.library.utils import *
from src.test.library.variables import *
import re
from src.test.library.excel_reader import data

def get_data():
        return data("test_data.xlsx","Hoja1")

def before_all(context):
    context.step_messages = []
    context.start_time=datetime.now()
    
    # Formatear la fecha y hora según el formato especificado
    formato = "%d %b %Y, %H:%M"
    context.fecha_formateada = context.start_time.strftime(formato)
    

def after_all(context):
    data_json_path= os.getcwd()+"\\json.pretty.output"

    with open(data_json_path, "a") as json_file:
        json_file.write("]") 
    
    with open(data_json_path, 'r') as file:
        data = json.load(file)

    # Modificar los nombres de los steps en el JSON
    modified_data = modify_json_with_message(data, context.step_messages)

    # Sobrescribir el archivo JSON con los cambios
    data_json_path = os.getcwd()+"\\New.pretty.output"

    with open(data_json_path, 'w') as file:
        json.dump(modified_data, file, indent=4)

    # Generate the HTML report
    data_json_path= os.getcwd()+"\\New.pretty.output"
    data = process_data_json(data_json_path)
    total_scenarios, total_steps, scenarios_information= count_total_scenarios_and_steps(data)
    report_folder = create_report_folder(template_folder_path, report_folder_path, source_files)
    count_assertions = count_non_empty_expected_cells(excel_path, expected_columns)

    generate_html_for_all_features(html_features_template, report_folder, data, total_scenarios, total_steps, scenarios_information, count_assertions)
    generate_html_for_each_feature(html_for_each_feature_template, report_folder, data)

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
    numero= ''
    patron= r'"(\d+)"'
    numero=re.findall(patron,scenario.name)
    if get_data()[int(numero[0])-1]["Ejecucion"] == "SI":
        if get_data()[int(numero[0])-1]["Escenario"]:
            scenario.name=get_data()[int(numero[0])-1]["Escenario"]    
    else:
        scenario.name="Escenario Skippeado"

    

def after_scenario(context, scenario):
    if context.state is not None:
        scenario.set_status("skipped")


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
    
