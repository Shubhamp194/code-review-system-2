"""
Setup script for AI Code Review System
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="ai-code-review",
    version="1.0.0",
    author="IBM Bob-a-thon Team",
    author_email="team@example.com",
    description="AI-Powered Code Review System using IBM Bob",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-org/bobathon-code-review",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Quality Assurance",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "code-review=src.analyzer.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["config/*.yaml"],
    },
)

# Made with Bob
