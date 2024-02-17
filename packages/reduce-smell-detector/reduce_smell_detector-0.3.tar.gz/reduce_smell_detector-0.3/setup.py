from setuptools import setup, find_packages

setup(
    name='reduce_smell_detector',
    version='0.3',
    packages=find_packages(),
    install_requires=[
        "PyYAML==6.0.1",
        "requests==2.31.0",
        "urllib3==2.2.0",
    ],
    entry_points={
        "console_scripts":[
            "detect_all_smells = reduce_smell_detector:detect_all",
        ],
    },
)