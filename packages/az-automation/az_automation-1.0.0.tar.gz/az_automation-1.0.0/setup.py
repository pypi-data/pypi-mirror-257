# setup.py

from setuptools import setup, find_packages

setup(
    name='az_automation',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # List your dependencies here
        'colorama',
    ],
    entry_points={
        'console_scripts': [
            'autoaz = az_auto.main:main',
        ],
    },
    author='Your Name',
    author_email='your.email@example.com',
    description='Your package description',
    long_description='Long description of your package',
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/az_auto',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
