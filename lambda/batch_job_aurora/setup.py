from setuptools import setup

setup(name='batch_job_aurora', version='1.0.0', packages=['.', 'data_types'], exclude=[
    "lambda_function"])
