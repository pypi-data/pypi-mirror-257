import io
import re
from os.path import dirname, join
from setuptools import find_packages, setup

def read(*names, **kwargs):
    with io.open(join(dirname(__file__), *names), encoding=kwargs.get('encoding', 'utf8')) as fh:
        return fh.read()

# Remove badges from README content
README_content = read('README.rst')
long_description = re.compile('^.. start-badges.*^.. end-badges', re.M | re.S).sub('', README_content)

setup(
    name='kivy_remote_control',
    version='0.0.0.1', 
    description='Kivy android joystick for mavsdk',
    long_description=long_description,
    packages=find_packages(where="src"),
    package_dir={'': 'src'},
    python_requires=">3.6, <=3.11",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    license='MIT',  # Add license information
    author='uberkie',  # Add author information
)
