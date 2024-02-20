from setuptools import setup

setup(
    name='helloiamaryan',
    version='0.1',
    py_modules=['helloiamaryan'],
    entry_points={
        'console_scripts': [
            'helloiamaryan = helloiamaryan:main'
        ]
    },
    author='Aryan',
    author_email='aryanmishra101112@gmail.com',
    description='A simple library that prints "I am Aryan"',
    license='MIT',
    keywords='helloiamaryan',
    url='https://github.com/aryantricks/helloiamaryan',
)
