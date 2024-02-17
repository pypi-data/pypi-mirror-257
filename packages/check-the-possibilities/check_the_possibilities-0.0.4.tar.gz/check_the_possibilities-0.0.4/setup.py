from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='check_the_possibilities',
    version='0.0.4',
    author='alexander_petrenko',
    author_email='gd@reseco.ru',
    description='This is the simplest module for print some text',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/AlexanderPetrenko83/prototype_python_library.git',
    packages=find_packages(),
    install_requires=[
         'pandas>=2.2.0'
    ],
    # classifiers=[
    #     'Programming Language :: Python :: 3.11',
    #     'License :: OSI Approved :: MIT License',
    #     'Operating System :: OS Independent'
    # ],
    # keywords='files speedfiles ',
    # project_urls={
    #     'GitHub': 'your_github'
    # },
    python_requires='>=3.12'
)
