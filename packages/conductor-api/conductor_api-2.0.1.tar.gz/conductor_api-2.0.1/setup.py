from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


def load_requirements(filename):
    with open(filename, 'r') as file:
        requirements = file.readlines()
        # Filter only the necessary runtime requirements for installation
        return [req for req in requirements if 'pytest' not in req and 'flake8' not in req]


def load_dev_requirements(filename):
    with open(filename, 'r') as file:
        requirements = file.readlines()
        # Get only the development/test requirements
        return [req for req in requirements if 'pytest' in req or 'flake8' in req]


setup(
    name="conductor_api",
    version=open('VERSION').read().strip(),
    description="A client to assist in connecting with the Conductor API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Dan Goodman",
    author_email="dgoodman@conductor.com",
    license="Apache 2.0",
    url="https://github.com/Conductor/searchlight-api-client-python",
    packages=find_packages(exclude="tests"),  # Adjust the paths to exclude as necessary
    install_requires=load_requirements('requirements.txt'),
    extras_require={
        'dev': load_dev_requirements('requirements.txt'),
    },
    python_requires='>=3.8',
    zip_safe=False
)
