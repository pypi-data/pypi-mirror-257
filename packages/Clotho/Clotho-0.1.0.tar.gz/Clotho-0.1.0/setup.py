from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()
setup(
    name="Clotho",
    version="0.1.0",
    author="CostasK",
    license="MIT",
    description="Proxy requests to AWS public endpoints and filter them using an allowlist",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ClothoProxy/PyClotho",
    py_modules=["clotho"],
    packages=find_packages(),
    install_requires=[requirements],
    python_requires=">=3.9",
    package_data={"": ["config.yaml.example"]},
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points="""
        [console_scripts]
        clotho=main:cli
    """,
    keywords="aws proxy cross-account security",
)
