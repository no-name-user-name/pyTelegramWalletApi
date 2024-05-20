from setuptools import setup, find_packages
from pathlib import Path

requirements = ["requests", "selenium-wire", "pytest"]
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='pyTelegramWalletApi',
    version='0.2.3',
    author='no-name-user-name',
    description='Telegram Wallet API',
    packages=find_packages(),
    install_requires=requirements,
    author_email='dimazver61@gmail.com',
    long_description=long_description,
    long_description_content_type='text/markdown'
)