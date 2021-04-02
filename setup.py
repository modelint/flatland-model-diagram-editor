"""Setup script for Flatland model diagram editor"""

import pathlib
import setuptools

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setuptools.setup(
    name="flatland-model-diagram-editor",
    version="0.21.0",
    description="Model text file + layout text file -> beautiful diagram",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/modelint/flatland-model-diagram-editor",
    author="Leon Starr",
    author_email="leon_starr@modelint.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=["pathlib", "SQLAlchemy", "pycairo", "Arpeggio", "numpy", ],
    entry_points={"console_scripts": ["flatland=flatland.__main__:main"]},
)