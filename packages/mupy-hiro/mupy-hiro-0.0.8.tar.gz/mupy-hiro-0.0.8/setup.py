from setuptools import setup

setup(
    name='mupy-hiro',
    version='0.0.8',
    packages=['mupy', 'mupy.utils', 'mupy.server', 'mupy.mutation', 'mupy.test_runners', 'mupy.mutation.finders',
              'mupy.mutation.mutators'],
    url='https://mupy.hirodiscount.com',
    license='APACHE 2.0',
    author='Jordan Nguejip',
    author_email='mupy@hirodiscount.com',
    description='A easy to use mutation analysis tool for beginners',
    keywords=['mutation', 'testing', 'ast', 'mutation testing', 'mutation analysis', 'faults', 'fault', 'fault base '
                                                                                                        'testing'],
    install_requires=['flask', 'flask_cors','graphviz'],
)
