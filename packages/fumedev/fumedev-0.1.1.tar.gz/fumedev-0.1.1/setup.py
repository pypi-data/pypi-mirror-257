from setuptools import setup, find_packages

with open('fumedev/requirements.txt') as f:
    required_packages = f.read().splitlines()

setup(
    name='fumedev',
    version='0.1.1',
    packages=find_packages(),
    install_requires=required_packages,
    package_data={
       'fumedev': ['my-languages.so', 'LICENSE', 'coder/LICENSE.txt'],
    },
    include_package_data=True,
    python_requires='>=3.6',
    author='Metehan Oz',
    author_email='metehanozdev@gmail.com',
    description='AI pair programmer',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': [
            'fumedev=fumedev.main:main',
        ],
    }
)
