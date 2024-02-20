from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

# with open(os.path.join(here, "README.md")) as f1:
#     description_1 = f1.read()

VERSION = '1.0.11'
DESCRIPTION = 'A utility for saving and loading data using pickle with logging functionality.'

setup(
    name="PickleHandler",
    version=VERSION,
    author="PRBN",
    author_email="<career.prabin@gmail.com>",
    url = 'https://github.com/Prbn/PickleHandler',
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
    # entry_points = {"consloe_scripts": ['PickleHandler = PickleHandler:PickleHandler']},
    keywords=['python', 'pickle', 'save', 'load', 'logging'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        # "License :: OSI Approved :: Creative Commons Attribution-ShareAlike 4.0 International License",
        "Operating System :: OS Independent",
    ]
)

# python setup.py sdist bdist_wheel
# python3.10 -m pip install dist\PickleHandler-1.0.4-py3-none-any.whl --force-reinstall
# python -m twine upload dist/* -p pypi-AgE-PRS-IcHlwaS5vcmcCJDNiMDYxNTcyLTk5NTAtNGQ1ZC1iODgxLTM0MDQ4MmFkN2UwNwACKlszLCJlYWFhYTRkMi1hZjAzLTQxMGItOTU1Mi03NTc3YTA2NDZmNDgiXQAABiAmps-eUUxqJfORyAQ99eyDzA8-Sekz_k0aA9pm9gb6YQ --verbose
# python -m twine upload -r testpypi dist/* -p pypi-AgE-PRS-NdGVzdC5weXBpLm9yZwIkYjVjMWRmN2QtZGVjZC00NDRkLTkwYTAtMjhiYmIwM2RmNDBkAAIqWzMsImQ3NGJlOTdjLWE4ZjYtNDFjZS1iYWE2LWMxOWQxOGY3OWY3ZiJdAAAGIJihmtmOvEFeV9nR01hE-dO0FIZkTIv8YZY0DlJ_dpt0 --verbose