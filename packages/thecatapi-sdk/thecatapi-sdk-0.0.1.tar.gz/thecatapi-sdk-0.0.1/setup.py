import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="thecatapi-sdk",
    version="0.0.1",
    author='Adavize Hassan',
    author_email="adavizeozorku@gmail.com",
    description="Python wrapper for making secure requests to TheCatAPI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ize-302/thecatapi-py-sdk",
    packages=setuptools.find_packages(),
    install_requires=['requests'],
    python_requires='>=3.12',
    project_urls={
        'Source': 'https://github.com/ize-302/thecatapi-py-sdk',
    },
)