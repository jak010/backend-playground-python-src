from behave import *


@given('한글한글한글')
def step_impl(context):
    pass


@when('we implement a test')
def step_impl(context):
    assert True is not False


@then('behave will test it for us!')
def step_impl(context):
    assert context.failed is False
