import setuptools

setuptools.setup(
    name="kayoc",
    version="0.0.3",
    packages=setuptools.find_packages(),
    install_requires=["requests==2.31.0", "aiohttp==3.9.3"],
    author="Pepijn van der Klei",
    author_email="pepijnvanderklei@gmail.com",
    description="A python client for the Kayoc API",
)
