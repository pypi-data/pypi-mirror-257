"""
Setup
"""
import os

from setuptools import setup, find_namespace_packages


DIST_NAME = "bosonic-jax"
PACKAGE_NAME = "bosonic_jax"

REQUIREMENTS = []

EXTRA_REQUIREMENTS = {
}

# Read long description from README.
README_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "README.md")
with open(README_PATH) as readme_file:
    README = readme_file.read()

version_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), PACKAGE_NAME, "VERSION.txt")
)

with open(version_path, "r") as fd:
    version_str = fd.read().rstrip()


setup(
    name=DIST_NAME,
    version=version_str,
    description=DIST_NAME,
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/EQuS/bosonic-jax",
    author="Shantanu Jha, Shoumik Chowdhury",
    author_email="shantanu.rajesh.jha@gmail.com",
    packages=find_namespace_packages(exclude=["tutorials*"]),
    install_requires=REQUIREMENTS,
    extras_require=EXTRA_REQUIREMENTS,
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Scientific/Engineering",
    ],
    keywords="quantum computing circuits",
    python_requires=">=3.7",
    project_urls={
        "Documentation": "https://github.com/EQuS/bosonic-jax",
        "Source Code": "https://github.com/EQuS/bosonic-jax",
        "Tutorials": "https://github.com/EQuS/bosonic-jax/tree/master/tutorials",
    },
    include_package_data=True,
)
