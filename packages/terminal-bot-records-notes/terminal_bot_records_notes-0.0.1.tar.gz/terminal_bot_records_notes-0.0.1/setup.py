from setuptools import setup, find_packages

setup(
    name='terminal_bot_records_notes',
    version='0.0.1',
    packages=find_packages(),
    license='MIT License',
    entry_points={
        'console_scripts': [
            'terminal_bot_records_notes=main:main'],
    },
    url='https://github.com/avtarso/python_core_21_team_11_project/tree/main',
    author='Avtarso',
    author_email='t0676352927@gmail.com',
    description='Command line bot personal assistant',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],

) 
