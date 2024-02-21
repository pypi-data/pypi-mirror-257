from setuptools import setup, find_packages

setup(
    name='web3x',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        "hdwallet",
        "requests",
        "web3",
        "typing"
        # List dependencies here
    ],
    author='john doe',
    author_email='xeallmail@mitico.org',
    description='Description of your package',
    url='https://github.com/yourusername/yourproject',
)
