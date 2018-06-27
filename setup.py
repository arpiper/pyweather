from setuptools import setup

with open('README.md', 'r') as rd:
    long_desc = rd.read()

setup(
    name='pyweather',
    version='0.1',
    description='Simple weather checking tool for toolbar output',
    long_description=long_desc,
    long_description_content_type='text/markdown',
    url='https://github.com/arpiper/pyweather',
    author='Andrew Piper',
    author_email='dev@arpiper.com',
    packages=['pyweatherarp'],
    classifiers=(
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
)
