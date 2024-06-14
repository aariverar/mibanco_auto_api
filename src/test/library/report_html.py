import json
from jinja2 import Template
import os
from datetime import datetime


def generate_html_report(test_results, output_file,fecha):
    # Load the template
    plantilla=os.getcwd()+"\\src\\test\\resources\\template\\report.html"
    with open(plantilla, 'r') as file:
        template_content = file.read()
    template = Template(template_content)
    
 # Process the test results
    data = []
    feature_data = {}
    for feature in test_results:
        feature_name = feature['name']
        scenarios = []
        scenario_passed_count = 0
        scenario_failed_count = 0
        scenario_skipped_count = 0

        for scenario in feature['elements']:
            scenario_name = scenario['name']
            status = scenario['status']
            steps = []

            if status == "passed":
                scenario_passed_count += 1
            elif status == "failed":
                scenario_failed_count += 1
            else:
                scenario_skipped_count += 1

            step_passed_count = 0
            step_failed_count = 0
            step_skipped_count = 0
            
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
                
                if step_status == "passed":
                    step_passed_count += 1
                elif step_status == "failed":
                    step_failed_count += 1
                else:
                    step_skipped_count += 1

                steps.append({'name': step_name,
                              'keyword': step_keyword, 
                              'status': step_status,
                              'message': step_message,
                              'duration': step_time})
                
            scenarios.append({'name': scenario_name, 
                              'status': status, 
                              'steps': steps})
            
        data.append({'feature_name': feature_name, 
                     'scenarios': scenarios,
                     'scenario_passed_count': scenario_passed_count,
                     'scenario_failed_count': scenario_failed_count,
                     'scenario_skipped_count': scenario_skipped_count,
                     'step_passed_count': step_passed_count, 
                     'step_failed_count': step_failed_count,
                     'step_skipped_count': step_skipped_count,
                     'scenarios_total': scenario_passed_count + scenario_failed_count+ scenario_skipped_count,
                     'steps_total': step_passed_count + step_failed_count + step_skipped_count})
  
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
rutareporte=os.getcwd()+"\\src\\test\\resources\\template\\report_final.html"
generate_html_report(test_results, rutareporte,fecha_formateada)
