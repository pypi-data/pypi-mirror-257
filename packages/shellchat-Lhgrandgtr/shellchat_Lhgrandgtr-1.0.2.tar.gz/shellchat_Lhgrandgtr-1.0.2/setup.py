from setuptools import setup, find_packages

setup(
    name='shellchat_Lhgrandgtr',
    version='1.0.2',
    packages=find_packages(),
    install_requires=[
        'prompt-toolkit',
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'shellchat=shellchat_Lhgrandgtr.main:main'
        ]
    }
)
