from setuptools import find_packages
from setuptools import setup


with open("requirements.txt") as f:
    required = f.read().splitlines()

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="fb_group_crawler",
    version="0.1",
    author="Henry Lee",
    author_email="henry410213028@gmail.com",
    install_requires=required,
    package_dir={"": "src"},
    packages=find_packages("src", exclude=["tests", "tools", "docs"]),
    include_package_data=True,
    description="An example project that crawl all the posts and comments in facebook public group page",
    long_description=long_description,
    license="MIT",
    entry_points={"console_scripts": ["fb_group_crawler=fb_group.run:main"]}
)