# setup.py

from setuptools import setup, find_packages

setup(
    name='insurance_predictor',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'xgboost>=1.0.0',
        'pandas',
    ],
    package_data={'insurance_predictor': ['data/*']},
    include_package_data=True,
    description='A package for predicting car insurance purchases using a pre-trained XGBoost model',
    author='Abdelrahman Al Omari',
    author_email='arya2@kent.ac.uk',
)
