from setuptools import setup, find_packages
import pathlib

setup(
    name="application_api",
    version="0.3",
    packages=find_packages(),
    include_package_data=True,
    description="API for student application",
    long_description=pathlib.Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    maintainer="John Gbaya-Kokoya",
    maintainer_email="gbayakokoyajohnjr@gmail.com",
    author="John Gbaya-Kokoya",
    author_email="gbayakokoyajohnjr@gmail.com",
    url="https://github.com/John-sys/student_application_api",
    license="MIT",
    keywords=["student", "application"],
    python_requires=">=3.6",
)
