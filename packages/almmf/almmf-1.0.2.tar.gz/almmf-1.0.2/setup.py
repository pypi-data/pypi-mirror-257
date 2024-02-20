import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "almmf",
    version = "1.0.2",
    author = "antho",
    author_email = "anthony.mcg24@gmail.com",
    description = "RAPIDS library with a collection of functions like sum, mean, max, min, etc",
    long_description = long_description,
    long_description_content_type = "text/plain",
    url = "https://github.com/AnthonyKsos/almmf",

    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    package_dir = {"": "src"},
    packages = setuptools.find_packages(where = "src"),
    python_requires = ">=3.6"
)