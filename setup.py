from setuptools import setup
from scandirRecursive import VERSION


def readme():
    with open("README.md", encoding="utf-8") as f:
        return f.read()


setup(
    name="scandirRecursive",
    version=VERSION,
    description="An os.scandir implementation with recursiveness",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/Alejandro-Roldan/scandirRecursive/tree/master",
    author="Alejandro Roldán",
    author_email="alej.roldan.trabajos@gmail.com",
    license="GPLv3",
    packages=["scandirRecursive"],
    zip_safe=False,
    python_requires=">=3.5",
)
