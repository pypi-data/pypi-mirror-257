from setuptools import setup, find_packages

with open('README.md','r') as f:
    description = f.read()

setup(
    name='FinRecipes',
    version='0.0.5',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=find_packages(),
    install_requires=[ 
        # Add dependencies here.
        'pandas',
        'progressbar',
        'yfinance',
        'stockstats',
        'datetime',
        'pytz',
        'numpy',
        'tables'
    ],

    long_description=description,
    long_description_content_type='text/markdown'
)
