from setuptools import setup, find_packages


with open("requirements.txt") as readme_file_1:
    install_requirements = readme_file_1.readlines()

with open("README.rst") as readme_file_2:
    readme = readme_file_2.read()

setup(
    name="thoughtful-common-packages",
    packages=find_packages(),
    install_requires=install_requirements,
    include_package_data=True,
    classifiers=[
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    description="The package contains all frequently used packages in Thoughtful",
    long_description_content_type="text/markdown",
    long_description=readme,
    keywords="thoughtful-common-packages",
    url="https://www.thoughtful.ai/",
    version="1.0.0",
)
