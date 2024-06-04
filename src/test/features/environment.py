# features/environment.py
import pandas as pd

def before_all(context):
    """
    Hook to execute before all tests.
    Use this to set up global context attributes, configurations, etc.
    """
    context.test_data = pd.read_excel('src/test/data/test_data.xlsx')
    print("Starting test suite execution...")
    print(context.test_data)

def after_all(context):
    """
    Hook to execute after all tests.
    Use this to clean up any resources initialized in before_all.
    """
    print("Finished test suite execution...")

def before_feature(context, feature):
    """
    Hook to execute before each feature.
    """
    print(f"Starting feature: {feature.name}")

def after_feature(context, feature):
    """
    Hook to execute after each feature.
    """
    print(f"Finished feature: {feature.name}")

def before_scenario(context, scenario):
    """
    Hook to execute before each scenario.
    """
    print(f"Starting scenario: {scenario.name}")  # Añade esto para depuración
    # Extraer el nombre del escenario base eliminando cualquier sufijo de índice
    scenario_base_name = scenario.name.split(" -- ")[0]
    # Find the row in the test data corresponding to the current scenario base name
    matching_rows = context.test_data[context.test_data['Scenario'].str.contains(scenario_base_name)]
    if not matching_rows.empty:
        scenario_data = matching_rows.iloc[0]
        context.endpoint = scenario_data['Endpoint']
        context.headers = dict([header.split(': ') for header in scenario_data['Headers'].split('\n')])
        context.request_type = scenario_data['Request Type']
        context.expected_status_code = scenario_data['Expected Status Code']
        context.expected_content = scenario_data['Expected Content']
    else:
        raise ValueError(f"No data found for scenario: {scenario_base_name}")

def after_scenario(context, scenario):
    """
    Hook to execute after each scenario.
    """
    print(f"Finished scenario: {scenario.name}")
    # You can add cleanup code here if necessary

def before_step(context, step):
    """
    Hook to execute before each step.
    """
    print(f"Starting step: {step.name}")

def after_step(context, step):
    """
    Hook to execute after each step.
    """
    print(f"Finished step: {step.name}")
    if step.status == "failed":
        # You can add code here to handle step failures
        print(f"Step failed: {step.name}")
