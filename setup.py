from setuptools import setup, find_packages

setup(
    name='django-cms-pagetags',
    version='0.1.4',
    description=('Tag fileds for CMS pages.'),
    keywords='django-cms django cms tags',
    author='Calin Furau',
    author_email='calin.furau@gmail.com',
    url='https://github.com/pbs/django-cms-pagetags',
    packages=find_packages(),
    include_package_data=True,
    install_requires = ['django-tagging==0.3.1'],

)
