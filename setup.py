import sys

from setuptools import setup, find_packages

install_requires = [
    'Jinja2',
    'Routes',
    'aiohttp',
]
if sys.version_info < (3, 4):
    install_requires.append('asyncio')


setup(
    name='induction',
    version='0.1',
    author='Bruno Renié',
    author_email='bruno@renie.fr',
    description='A simple web framework based on asyncio.',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    install_requires=install_requires,
    packages=find_packages(exclude=['tests']),
    test_suite='tests',
)
