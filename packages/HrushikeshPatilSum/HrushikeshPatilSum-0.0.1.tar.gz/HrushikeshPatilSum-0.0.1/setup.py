from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 11',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='HrushikeshPatilSum',
    version='0.0.1',
    description='A very basic package with Sum function',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Hrushikesh Patil',
    author_email='hrushi6161@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='sum',
    packages=find_packages(),
    install_requires=['']
)