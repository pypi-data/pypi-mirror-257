from setuptools import setup, find_packages

setup(
    name='plasma-fhir-client-py',
    version='0.0.1',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    # include any other necessary metadata
)


from setuptools import setup, find_packages

setup(
    name='plasma-fhir-client-py',
    version='0.0.1',
    author='Eric Morgan',
    author_email='plasmafhir@gmail.com',
    description='Plasma FHIR Python Client',
    long_description=open('README.md').read(),  # A long description from README.md
    long_description_content_type='text/markdown',  # Specifies the long desc content type
    url='https://github.com/PlasmaHealth/plasma-fhir-client-py',  # URL to your package's repo
    package_dir={'': 'src'},  # Tells setuptools that packages are under src
    packages=find_packages(where='src'),  # Automatically find packages in src
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Minimum version requirement of Python
    install_requires=[
        'requests>=2.19.1',
        'base64>=1.0.0',
    ],
)
