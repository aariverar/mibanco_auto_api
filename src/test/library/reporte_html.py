import json
from jinja2 import Template
import os
from datetime import datetime


def generate_html_report(test_results, output_file,fecha):
    # Load the template
    plantilla=os.getcwd()+"\\src\\test\\resources\\template\\report2.html"
    with open(plantilla, 'r') as file:
        template_content = file.read()
    template = Template(template_content)
    
 # Process the test results
    data = []
    for feature in test_results:
        feature_name = feature['name']
        scenarios = []
        for scenario in feature['elements']:
            scenario_name = scenario['name']
            status = scenario['status']
            steps = []
            for step in scenario['steps']:
                step_name = step['name']
                step_keyword = step['keyword']
                if 'result' in step:
                    step_status = step['result'].get('status', 'unknown')  # Usa 'unknown' como valor predeterminado
                    step_message = step['result'].get('message', '')  # Usa una cadena vacía como valor predeterminado
                    step_time = step['result'].get('duration', 0)  # Usa 0 como valor predeterminado si no existe 'duration'
                else:
                    step_status = 'failed'
                    step_message = 'failed'
                    step_time = 0
                #step_status = step['result']['status']
                #step_message=step['result']['message']
                #step_time=step['result']['duration']
                steps.append({'name': step_name,'keyword':step_keyword, 'status': step_status,'message': step_message,'duration':step_time})
            scenarios.append({'name': scenario_name, 'status': status, 'steps': steps})
        data.append({'feature_name': feature_name, 'scenarios': scenarios})

 
    # Render the template with the test data
    html_output = template.render(features=data,date=fecha)

    # Write the HTML output to a file
    with open(output_file, 'w') as file:
        file.write(html_output)


rutaJson= os.getcwd()+"\\Nuevo.pretty.output"

# Load the test results JSON
with open(rutaJson, 'r') as file:
    test_results = json.load(file)
   #print(data)

ahora = datetime.now()

# Formatear la fecha y hora según el formato especificado
formato = "%d %b %Y, %H:%M"
fecha_formateada = ahora.strftime(formato)

# Generate the HTML report
rutareporte=os.getcwd()+"\\src\\test\\reports\\test_report2.html"
generate_html_report(test_results, rutareporte,fecha_formateada)
