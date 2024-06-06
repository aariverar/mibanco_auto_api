import json
from jinja2 import Template
import os


def generate_html_report(test_results, output_file):
    # Load the template
    plantilla=os.getcwd()+"\\src\\test\\resources\\template\\report.html"
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
                step_status = step['result']['status']
                step_message=step['result']['message']
                steps.append({'name': step_name, 'status': step_status,'message': step_message})
            scenarios.append({'name': scenario_name, 'status': status, 'steps': steps})
        data.append({'feature_name': feature_name, 'scenarios': scenarios})

    #print(data)
    # Render the template with the test data
    html_output = template.render(features=data)

    # Write the HTML output to a file
    with open(output_file, 'w') as file:
        file.write(html_output)


rutaJson= os.getcwd()+"\\Nuevo.pretty.output"

# Load the test results JSON
with open(rutaJson, 'r') as file:
    test_results = json.load(file)


# Generate the HTML report
generate_html_report(test_results, 'test_report.html')
