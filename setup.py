'''

its an essential part of packaging and distributing python projects
its used to defione the configuration of your project such as its dependencies and more

'''


from setuptools import find_packages, setup
from typing import List

HYPEN_E_DOT = "-e ."

def get_requirements(file_path: str) -> List[str]:
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.strip() for req in requirements if req.strip()]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)

    return requirements
'''set up meta data'''
setup(
    name="ML Project",
    version="0.0.1",
    author="Anas",
    author_email="qazi7784@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements("requirements.txt")
)