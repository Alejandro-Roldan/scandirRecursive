from setuptools import setup
import scandirRecursive


def readme():
    with open("README.md", encoding="utf-8") as f:
        return f.read()


setup(
    name="scandirRecursive",
    version=scandirRecursive.__version__,
    description="An os.scandir implementation with recursiveness",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/Alejandro-Roldan/scandirRecursive/tree/master",
    author=scandirRecursive.__author__,
    author_email=scandirRecursive.__email__,
    license=scandirRecursive.__license__,
    packages=["scandirRecursive"],
    entry_points={
        "console_scripts": [
            "scandirrecursive = scandirRecursive.scandirrecursive:cli_run"
        ]
    },
    package_data={},
    zip_safe=False,
    python_requires=">=3.5",
)
