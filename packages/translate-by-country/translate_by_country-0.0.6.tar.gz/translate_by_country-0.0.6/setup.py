from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()



setup(
    name='translate_by_country',  
    version= '0.0.6', 
    description='A library to translate text by country information',
    long_description=readme,
    author='Sina157',  
    packages=find_packages(),
    author_email='sina.shams@yahoo.com', 
    url='https://github.com/Sina157/translate-by-country',  
    install_requires=[
     'googletrans==4.0.0-rc1'
    ],
    entry_points={}
)
