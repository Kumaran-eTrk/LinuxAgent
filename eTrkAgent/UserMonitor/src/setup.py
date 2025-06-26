import os
from setuptools import setup

base_dir = os.path.abspath(os.path.dirname(__file__))
with open('requirements.txt') as f:
    requirements = f.read().splitlines()
setup(
    name='MonitorUser',
    version='0.1',
    packages=['utils'], 
    package_data={'MonitorUser': ['*.py']},
    # install_requires=['wheel', 'bar', 'greek'],
    install_requires=requirements,
    setup_requires=['wheel'],  

    entry_points={
            'console_scripts': [
             'MonitorUser=utils.agent:run',
        ],
    
    },
   
     scripts=[os.path.join(base_dir,  'utils', 'agent.py')],
     data_files=[('bin', [os.path.join(base_dir,  'config', 'config.ini')])]
    )
