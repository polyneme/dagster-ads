from setuptools import find_packages, setup

with open("README.md") as f:
    long_description = f.read()

with open("requirements.in") as f:
    install_requires = f.read().splitlines()

with open("requirements.dev.in") as f:
    dev_requires = f.read().splitlines()[1:]  # Elide `-c requirements.txt` constraint

setup(
    name="dagster_ads",
    url="https://github.com/polyneme/dagster-ads",
    packages=find_packages(
        exclude=["dagster_ads_tests"]
    ),
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    author="Donny Winston",
    author_email="donny@polyneme.xyz",
    description="Dagster code location for Astrophysics Data System (ADS) software-defined assets.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
    ],
    install_requires=install_requires,
    extras_require={
        "dev": dev_requires,
    },
    python_requires=">=3.10",
    entry_points={"console_scripts": []},
)