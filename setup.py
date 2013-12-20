from setuptools import setup, find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGELOG = open(os.path.join(here, 'CHANGELOG.txt')).read()


version = '0.1'

install_requires = [
    'Jinja2',
]

tests_requires = [
    'mock',
    'nose',
]

setup(name='filereaper',
    version=version,
    description="A flexible file reaper that support multiple removal policies",
    long_description=README + '\n\n' + CHANGELOG,
    classifiers=[
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: MIT License",
    ],
    keywords='file removal reaper multiple policies',
    author='Victor Garcia',
    author_email='bravejolie@gmail.com',
    url='http://github.com/victorgp/filereaper',
    license='MIT',
    packages=find_packages('src'),
    package_dir = {'': 'src'},include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    tests_requires=tests_requires,
    test_suite='tests.unit',

)
