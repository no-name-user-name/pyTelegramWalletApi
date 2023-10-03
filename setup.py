from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["requests", "selenium-wire", "pytest"]

setup(
    name='pyTelegramWalletApi',
    version='0.2',
    author='no-name-user-name',
    description='Telegram Wallet API',
    packages=find_packages(),
    install_requires=requirements,
    author_email='dimazver61@gmail.com',
)