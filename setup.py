import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='jtbl',
    version='1.1.7',
    author='Kelly Brazil',
    author_email='kellyjonbrazil@gmail.com',
    description='A simple cli tool to print JSON and JSON Lines data as a table in the terminal.',
    install_requires=[
        'tabulate>=0.8.6'
    ],
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.6',
    url='https://github.com/kellyjonbrazil/jtbl',
    packages=setuptools.find_packages(exclude=['*.tests', '*.tests.*', 'tests.*', 'tests']),
    entry_points={
        'console_scripts': [
            'jtbl=jtbl.cli:main'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Utilities'
    ]
)
