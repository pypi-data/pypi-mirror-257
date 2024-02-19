import setuptools

with open("requirements.txt", "r") as file:
    requirements = file.readlines()

setuptools.setup(
    name="kayoc",
    version="0.0.1",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    author="Pepijn van der Klei",
    author_email="pepijnvanderklei@gmail.com",
    description="A python client for the Kayoc API",
)
