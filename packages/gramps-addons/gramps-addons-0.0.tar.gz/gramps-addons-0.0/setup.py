"""
Placeholder for a Gramps GitHub repository in PyPI.
"""

from setuptools import setup

with open("README.md", "r") as f:
    readme_text = f.read()

setup(
    name="gramps-addons",
    url="https://github.com/gramps-project/addons",
    version="0.0",
    description="Addons for the Gramps genealogy program",
    long_description=readme_text,
    long_description_content_type="text/markdown",
    author="The Gramps Project",
    author_email="nick-h@gramps-project.org",
    scripts=["gramps.py"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Topic :: Sociology :: Genealogy",
    ],
)
