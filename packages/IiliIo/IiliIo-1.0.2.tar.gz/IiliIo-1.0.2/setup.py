from setuptools import setup, find_packages
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
readme_path = os.path.join(current_dir, 'README.md')

setup(
    name='IiliIo',
    version='1.0.2',
    description='IiliIo uploader without API key',
    author='OneFinalHug',
    author_email='voidlillis@gmail.com',
    url='https://github.com/OneFinalHug/IiliIo/',
    long_description = open(readme_path).read(),
    long_description_content_type='text/markdown',
    keywords=['IiliIo_uploader', 'telegram','host', 'uploader', 'IiliIo', 'image'],
    packages=find_packages(),
    install_requires=[
        'requests',
        'colorclip',
		'fake-useragent',
		'requests-toolbelt'
    ],
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    license='MIT',
    entry_points={
        'console_scripts': [
            'IiliIo = IiliIo:main'
        ]
    }
)
