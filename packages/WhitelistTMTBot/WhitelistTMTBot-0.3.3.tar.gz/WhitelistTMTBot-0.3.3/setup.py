from setuptools import find_packages, setup


def readme():
    with open("README.md", "r") as f:
        return f.read()


setup(
    name="WhitelistTMTBot",
    version="0.3.3",
    author="nmmodi",
    author_email="mniyazkhanov@gmail.com",
    description="This is the simplest module for quick work with telegram bots.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://gitlab.com/nmModi/whitelist_tmt_bot.git",
    packages=find_packages(),
    install_requires=["requests==2.31.0"],
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="telegram bot",
    project_urls={},
    python_requires=">=3.6",
)
