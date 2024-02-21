from setuptools import setup, find_packages
import pycinante

requirements = [
    'setuptools~=68.2.2',
    'python-archive~=0.2',
    'cryptography~=41.0.7',
    'numpy~=1.23.0',
    'matplotlib~=3.7.4'
]

setup(
    name='pycinante',
    version=pycinante.__version__,
    python_requires='>=3.8',
    author='Chisheng Chen',
    author_email='chishengchen@126.com',
    url='https://github.com/gndlwch2w/pycinante',
    description='Python\'s Rocinante for easily programming.',
    license='MIT-0',
    packages=find_packages(),
    zip_safe=True,
    install_requires=requirements, )
