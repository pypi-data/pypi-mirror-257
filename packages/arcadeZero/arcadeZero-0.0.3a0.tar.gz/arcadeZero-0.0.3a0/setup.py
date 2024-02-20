from setuptools import setup, find_packages

setup(
    name="arcadeZero",
    version="0.0.3a0",
    author="emhang",
    author_email="emhang@126.com",
    description="A more user-friendly version of the arcade game library, especially designed for Huanma Python Course.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=[
        "arcade==2.6.17"]
)
