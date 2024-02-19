import setuptools

with open("README.md", "r",encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="evext",
    version="1.0.0",
    author="Apple.Pie.etc",
    author_email="",
    description="A calculate Python package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/suberstring/evext",
    packages=setuptools.find_packages(),
    install_requires=[],
    entry_points={},
    classifiers=(
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)