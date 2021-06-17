from setuptools import setup, find_packages
from scxml_to_c import __version__ as version


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="scxml_to_c",
    version=version,
    author="Donny Zimmanck",
    author_email="dzimmanck@enphaseenergy.com",
    description="Translation libracy for converting SCXML (State Chart XML) files to ANSI-C for embedded applications.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dzimmanck/scxml_to_c",
    packages=find_packages(),
    install_requires=[
        "lxml >= 4.6.3",
        "csnake >= 0.3.1"
    ],
    extras_require={'dev': [
                        "pytest",
                        "pytest-benchmark",
                        "tox",
                        "coverage[toml]"]},
    python_requires=">=3.6",
    entry_points={
            'console_scripts': [
                'scxml_to_c = scxml_to_c.main:_convert',
            ]
    }
)
