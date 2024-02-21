import os
from setuptools import setup, find_packages


if __name__ == '__main__':
    env_value = os.environ.get('MY_SUPER_ENV')

    assert env_value, "MY_SUPER_ENV should be set in order to build wheel"


    setup(
        name='env_test_package',
        version='0.0.3',
        author='Nichita Morcotilo',
        author_email='nmorkotilo@gmail.com',
        description='Package created to test passing env variables',
        packages=['env_test_package'],
        classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        ],
        python_requires='>=3.8',
    )