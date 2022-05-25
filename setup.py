"""setup the package."""
import sys

import setuptools

needs_pytest = {"ptr", "pytest", "test"}.intersection(sys.argv)
pytest_runner = ["pytest-runner"] if needs_pytest else []

setuptools.setup(
    name="phrase-counter",
    version="0.1.6",
    author="Reza Shabrang",
    author_email="rezashabrang.m@gmail.com",
    url="https://github.com/rezashabrang/common-phrase-detection",
    description="""A package for counting ngrams in a text.""",
    license="MIT",
    packages=setuptools.find_packages(
        exclude=["_common_phrase_detection_tests", "*.__pycache__"]
    ),
    python_requires=">=3.8",
    install_requires=[
        "cleaning-utils", "beautifulsoup4", "requests", "scikit-learn",
        "pandas", "polyglot", "PyICU", "pycld2"
    ],
    tests_require=["pytest"],
    extras_require={
        "tests": [
            "flake8",
            "pytest",
            "pytest-cov",
            "pytest-flake8",
            "pip",
            "bandit",
            "black",
            "coverage",
            "coverage-badge",
            "darglint",
            "isort",
            "mypy",
            "mypy-extensions",
            "pre-commit",
            "pydocstyle",
            "pylint",
            "pytest-html",
            "pyupgrade",
            "safety",
            "radon",
            "docstr-coverage",
        ],
    },
    setup_requires=[] + pytest_runner,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
