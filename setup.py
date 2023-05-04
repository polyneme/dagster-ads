from setuptools import find_packages, setup

setup(
    name="dagster_ads",
    packages=find_packages(exclude=["dagster_ads_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud"
    ],
    extras_require={"dev": ["dagit", "pytest"]},
)
