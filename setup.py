from setuptools import find_packages, setup


setup(
    name='mistools',
    packages=find_packages(include=['mistools', 'mistools.lib']), # include root module and local modules sub dirs with __init__ files...
    package_data={'mistools' : ['spec/mis_spec.json']},                 # include local config/data files from LIB_ROOT
    version='1.0.0',
    description='Library containing tools for working with MIS Data',
    author='Jared Arnold',
    license='MIT',
    install_requires=['pyodbc'],                                                # include non-native third party python modules ...pyodbc...if we used it here
    setup_requires=[],
    tests_require=[],                                                   # do not distribute tests a dev can grab them from git for now
)
