from setuptools import setup, find_packages

setup(
    name='testing_phase_pipme',
    version='1.2.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [ 'pipme = pipme.main:run_cli' ]
    },
    install_requires=[
        
    ],
)
