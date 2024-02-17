from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='parsec_integration',
    version='0.0.1',
    author='FuR1DeV',
    author_email='vasia19rus@bk.ru',
    description='This is the package for integration of ASBP with Parsec',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/FuR1DeV',
    packages=find_packages(),
    install_requires=['pydantic>=2.5.3', 'zeep>=4.2.1'],
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='parsec integration asbp',
    project_urls={
        'GitHub': 'https://github.com/FuR1DeV'
    },
    python_requires='>=3.10'
)
