from setuptools import setup, find_packages

setup(
    name='eng_dic',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests>=1.1.1'
    ],
    entry_points={
        "console_scripts":[
            "eng_dic=eng_dic:Meaningof"
        ]
    }
)