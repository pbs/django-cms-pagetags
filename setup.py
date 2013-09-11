from setuptools import setup, find_packages

setup(
    name='django-cms-pagetags',
    version='0.1.7',
    description=('Tag fileds for CMS pages. Works with django-tagging or django-tagging-ng.'),
    keywords='django-cms django cms tags',
    author='Calin Furau',
    author_email='calin.furau@gmail.com',
    url='https://github.com/pbs/django-cms-pagetags',
    packages=find_packages(),
    include_package_data=True,
    setup_requires = ['s3sourcepackages'],
    install_requires = ['django-tagging==0.3.1'],
    extras_require = {
        'multilang': ['django-tagging-ng'],
    },
    license='BSD License',
)
