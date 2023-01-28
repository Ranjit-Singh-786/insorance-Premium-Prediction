from setuptools import find_packages,setup
from typing import List

# to define all the dependency in our project by the setup.py file.
requirement_filePath = 'requirements.txt'
editable_indiacator = '-e .'
def get_requirements()->list[str]:
    with open(requirement_filePath) as requirementFile:
        requirement_list = requirementFile.readlines()
    requirement_list = [requirement.replace("\n","") for requirement in requirement_list]
    # removing the editable_indicator from the requirements
    if editable_indiacator in requirement_list:
        requirement_list.remove(editable_indiacator)
    return requirement_list


setup(name='insurance',
      version='0.0.1', # every time when you will release your next time your project u wil have to change the version.
      description='insurance premium prediction ML project.',
      author='Ranjit Singh',
      author_email='jiradhey402@gmail.com',    # mail must be associated with git
      packages=find_packages(),     # it will find all the packages from your project.
      install_reqires =get_requirements()  # varaible assigned by itself. to give the idea about dependencies.
)