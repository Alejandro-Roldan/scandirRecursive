from setuptools import setup

import scandirrecursive


def readme():
    with open("README.md", encoding="utf-8") as f:
        return f.read()


setup(
    name="scandirRecursive",
    version=scandirrecursive.__version__,
    description="An os.scandir implementation with recursiveness",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/Alejandro-Roldan/scandirRecursive/tree/master",
    author=scandirrecursive.__author__,
    author_email=scandirrecursive.__email__,
    license=scandirrecursive.__license__,
    packages=["scandirrecursive"],
    entry_points={
        "console_scripts": [
            "scandirrecursive = scandirrecursive.scandirrecursive:cli_run"
        ]
    },
    package_data={},
    zip_safe=False,
    python_requires=">=3.5",
)
