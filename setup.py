from setuptools import setup, find_packages

setup(
    name='FastGATE Tools',
    version='0.1',
    long_description=__doc__,
    packages=find_packages(),
    install_requires=['requests', 'Click'],
    entry_points='''
        [console_scripts]
        fastgate=fastgate:cli
    ''',
)
