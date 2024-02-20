from setuptools import setup, find_packages
from pathlib import Path

parser_result_files = [str(path.relative_to('parser_result')) for path in Path('parser_result').rglob('*')]

setup(
    name="cfx_middleware",
    version="1.6",
    packages=find_packages(),
    package_data={'': parser_result_files},
    install_requires=["python-dotenv"],
    python_requires=">=3",
    author="Victor Dominguez",
    author_email="e-victor_dominguez@usiglobal.com",
    description="Provide a Middleware between the system and CFX",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://dev.azure.com/USI-Applications/USI%20Global%20Development/_git/PCD.Middleware.CFX.Python",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
