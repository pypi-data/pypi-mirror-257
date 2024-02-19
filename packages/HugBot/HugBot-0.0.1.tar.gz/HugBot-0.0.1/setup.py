from setuptools import setup, find_packages

setup(
    name='HugBot',
    version='0.0.1',
    author='Eugene Evstafev',
    author_email='chigwel@gmail.com',
    description='Automated interactions with Hugging Face Chat using Selenium',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/chigwell/HugBot',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'selenium',
        'webdriver-manager'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
