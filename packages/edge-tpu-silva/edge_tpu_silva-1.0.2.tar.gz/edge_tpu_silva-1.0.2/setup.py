from setuptools import setup, find_packages

setup(
    name='edge_tpu_silva',
    version='1.0.2',
    packages=find_packages(),
    install_requires=[
        # List your dependencies here
    ],
    entry_points={
        'console_scripts': [
            'silvatpu = edge_tpu_silva:main',
        ],
    },
)

# python setup.py sdist bdist_wheel