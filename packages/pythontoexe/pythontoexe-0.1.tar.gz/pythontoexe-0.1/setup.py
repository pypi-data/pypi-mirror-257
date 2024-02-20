from setuptools import setup, find_packages

setup(
    name='pythontoexe',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'pythontoexe = pythontoexe.hello:say_hello'
        ]
    }
)
