# features/environment.py
import pandas as pd

def before_all(context):
    """
    Hook to execute before all tests.
    Use this to set up global context attributes, configurations, etc.
    """

def after_all(context):
    """
    Hook to execute after all tests.
    Use this to clean up any resources initialized in before_all.
    """

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
    if step.status == "failed":
        # You can add code here to handle step failures
        print(f"Step failed: {step.name}")
