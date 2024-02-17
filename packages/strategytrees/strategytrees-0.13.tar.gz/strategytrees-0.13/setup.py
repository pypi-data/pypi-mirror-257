from setuptools import setup, find_packages

setup(
    name='strategytrees',
    version='0.13',
    packages=find_packages(),
    description='Evolving trading strategy trees using genetic algorithm',
    author='Oliver Hitchcock',
    author_email='',
    license='MIT',
    install_requires=[
        'pandas==1.5.2',
        'numpy==1.26.3'
    ],
    classifiers=[
        # Package classifiers (https://pypi.org/classifiers/)
          'Programming Language :: ML'
    ],
)
