import re

import setuptools
from setuptools import find_packages

with open("./autodistill_yolo_world/__init__.py", "r") as f:
    content = f.read()
    # from https://www.py4u.net/discuss/139845
    match = re.search(r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]', content)
    version = match.group(1) if match else None

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="autodistill_yolo_world",
    version=version,
    author="Lakshman",
    author_email="lakshman@moiiai.com",
    description="Yolo-World module for use with Autodistill",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lakshmanmoiiai/autodistill-yolo-world",
    install_requires=[
        "torch",
        "supervision",
        "numpy",
        "ultralytics",
        "autodistill",
        "roboflow",
    ],
    packages=find_packages(exclude=("tests",)),
    extras_require={
        "dev": ["flake8", "black==22.3.0", "isort", "twine", "pytest", "wheel"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
