from setuptools import setup

requires = [
    'six'
]

tests_require = [
    'mock',
    'pytest',
    'pytest-cov'
]

setup(
    name='findb',
    version='0.1',
    description='A very basic Key-Value Database.',
    url='http://github.com/joshfinnie/findb',
    author='Josh Finnie',
    author_email='josh@jfin.us',
    license='MIT',
    packages=['findb'],
    zip_safe=False,
    install_requires=requires,
    tests_require=tests_require,
    classifiers=(
        'Natural Language :: English',
        'License :: OSI Approved :: MIT',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    )
)
