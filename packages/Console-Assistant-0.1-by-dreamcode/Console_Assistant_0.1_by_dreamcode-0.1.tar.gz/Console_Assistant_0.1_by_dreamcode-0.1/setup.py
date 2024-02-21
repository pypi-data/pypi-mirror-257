from setuptools import setup

setup(
    name='Console_Assistant_0.1_by_dreamcode',
    version='0.1',
    description='This application is a universal manager that combines the functions of a contact, note, event and file manager to conveniently manage various aspects of information.',
    url='https://github.com/AkaVelial13/PythonProject.git',
    author='Dreamcode team, Vitaliy Nerg, Omelchenko Anton, Artem Hrytsay, Serhii Nozhenko, Muzychuk Vadym',
    author_email='occultnerg2@gmail.com, omelchenko230783@gmail.com, artem_madrid@hotmail.com, neprokaren41@gmail.com, gr.fyntik@gmail.com',
    license='MIT',
    install_requires=[
        'tabulate'
    ],
    entry_points={
        'console_scripts': [
            'assistant = src.main:main',
        ],
    },  
    zip_safe=False
)
