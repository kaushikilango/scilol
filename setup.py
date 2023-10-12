from setuptools import find_packages,setup
from typing import List

def get_requirements(file:str) -> List[str]:
    requirements = []
    with open(file,'r') as f:
        requirements = f.readlines()
        requirements = [requirement.replace('\n','') for requirement in requirements]

        if '-e .' in requirements:
            requirements.remove('-e .')
    return requirements



setup(
    name = 'scilol',
    version = '0.0.1',
    description = 'A package for scilol',
    author = 'Kaushik Ilango',
    author_email = 'kilango5@outlook.com',
    packages = find_packages(),
    install_requires = get_requirements('requirements.txt'),
)