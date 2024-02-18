from setuptools import setup

setup(
    name='attack',
    version='0.1',
    py_modules=['attack'],
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'cybervpn=cybervpn.main_script:main',
        ],
    },
)

