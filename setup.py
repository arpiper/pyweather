from setuptools import setup, find_namespace_packages

with open('README.md', 'r') as rd:
    long_desc = rd.read()

setup(
    name='pyweatherarp',
    version='1.1.1',
    description='Simple weather checking tool for toolbar output',
    long_description=long_desc,
    long_description_content_type='text/markdown',
    url='https://github.com/arpiper/pyweather',
    author='Andrew Piper',
    author_email='dev@arpiper.com',
    package_dir={"": "src"},
    packages=find_namespace_packages(where='src'),
    entry_points={
        'console_scripts': [
            'pyweatherarp = main:__main__.main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
    ],
)
